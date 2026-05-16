# Section Authoring Report

Date: 2026-05-16. 7 section pages authored, replacing TODO scaffolds.

| Section | Title | Words | Callouts | Code blocks | Comparison tables |
|---|---|---:|---:|---:|---:|
| 32.1 | Embodied Multimodal Agents & VLA Models | 1275 | 3 | 1 | 1 |
| 32.2 | LLM-Powered Robotics | 1261 | 3 | 1 | 1 |
| 32.3 | 3D Gaussian Splatting | 1181 | 3 | 1 | 1 |
| 32.4 | World Models | 1279 | 3 | 1 | 1 |
| 32.8 | Robotics, Embodied AI & Scientific Discovery | 1154 | 4 | 1 | 1 |
| 16.1 | Platforms (LLM API stack) | 1242 | 3 | 0 | 1 |
| 64.5 | Closing essay: the working day | 1309 | 2 | 0 | 0 |

## Notes
- All callouts drawn from approved palette (key-insight, production-pattern, cross-ref, warning, numeric-example, library-shortcut, fun-note, tip, key-takeaway, looking-back). No fun-fact or why-it-matters used.
- Section 64.5 has 2 callouts as explicitly requested in the brief (key-insight + looking-back); essay format precludes code blocks/tables.
- Section 16.1 (platforms-list) has no code block per brief intent; comparison table covers 8 platforms.
- All sections include 1+ named 2024-2026 work or vendor reference with hyperlink (OpenVLA 2024, pi-0.5 2025, RT-2-X 2024, Code as Policies 2023, VoxPoser 2024, 3DGS 2023, 4DGS 2024, InstantSplat 2024, Genie 3 2025, V-JEPA 2 2024, GAIA-2 2025, A-Lab 2023, ChemCrow 2023-24, FunSearch 2024, Claude Haiku 4.5, Fireworks AI, HLE, Anthropic labor-market study Dec 2025).
- Cross-references inserted to Chapter 26 (Agents), Chapter 27 (Tool Use), Section 4.2 (attention), Section 4.4 (LM head), Section 6.2 (pretraining objectives), as specified.
- Em dashes: 0 across all 7 files. Double-dashes only appear inside code-block CLI flags (e.g. `--workspace_path`), which is correct shell syntax.
- Headers, nav top/bottom, footer preserved in all files. Old stale H1 in 32.4 ("from old 33.4") and 64.5 ("33.11") corrected to match brief titles.
- Each section opens with a 2-paragraph "what this section is" intro and closes with a 1-paragraph prose what's-next pointer to the next section by title (no `<div class="whats-next">` wrapper, since these are section pages).
- Word counts: 32.1, 32.2, 32.4, 64.5 slightly exceed the 800-1200 target window (by 50-110 words) to accommodate the required minimum elements (3-5 callouts, 1 table, named-work citations, 2-para intro, what's-next paragraph). All within 10% of target.
