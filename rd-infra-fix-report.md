# R&D Infrastructure Restructure: Fix Report

Executed against the audit at `rd-infrastructure-duplication-audit.md`. Scope: appendices H, I, J, K only.

## Concrete changes

1. **H.1 (Essential Libraries)**: stripped the `wandb.init/log/finish` mini-snippet (formerly lines 286-295) and replaced it with a cross-reference callout pointing to `appendix-k-experiment-tracking/section-k.1.html`. The `wandb` row in the libraries table is preserved as recognition-context only.
2. **I.3** renamed from "Python Environment Setup" to "Linking CUDA to PyTorch (Wheels and Channels)". Deleted duplicate venv/conda creation recipes (formerly lines 35-65), now back-referenced to `H.2`. New body covers the conda `pytorch-cuda` channel, the pip `--index-url` flag, the driver/wheel compatibility table (cu121/cu124/cu126), and an NCCL multi-GPU warning.
3. **J.3** retitled "Linking Experiment Runs to Git Commits". Old W&B+MLflow body deleted. New body introduces three patterns: `git_sha()` helper for tracker config, `git describe --dirty` for working-tree detection, and per-run `git tag run/<id>` for milestone runs. Each pattern has a code fragment (J.3.1-J.3.3) and links to Appendix K for the tracker APIs themselves.
4. **K.2 section 5** (MLflow Projects): the Git-URL invocation (formerly `mlflow.run("https://github.com/...")`) and the "Run a project from a Git repo" comment are removed. Replaced with a YAML-rendered MLproject sample, a configuration-management framing, and a cross-ref callout to J.4 for Git-driven invocation.
5. **K.4 M.4.6 (CI/CD Integration)**: full GitHub Actions YAML and `validate_model.py` deleted. Replaced with a cross-ref callout to J.4 (with a clear "K owns which version, J owns how to deploy" split rule).
6. **J.4** retitled "Reproducibility and CI/CD for ML". The CI/CD recipe moved here in a new subsection "MLOps Plumbing: GitHub Actions for Model Deployment", including the workflow YAML (J.4.3) and validator script (J.4.4). Stale "Continue to Appendix K: Glossary" already updated by linter to point to Appendix K; the prev-link nav-title fixed. Takeaways list updated to reference J.3 instead of duplicating K's tracker advice.
7. **Index files (H/I/J/K)**: section-card prefixes corrected from C/D/E/L to H/I/J/K. Big-Picture and When-to-Use paragraphs updated where they referenced the old letters or old section titles. I-index expanded from 6 to 8 sections.
8. **I.6 / I.7 / I.8**: existing `section-i.6.html` (Verifying Your Setup) copied to `section-i.8.html` and re-numbered. New `section-i.6.html` written as placeholder for "IDE Setup and Editor Integrations" (planned-coverage stub: VS Code, Cursor, PyCharm, Jupyter, remote dev, workspace hygiene). New `section-i.7.html` written as placeholder for "API Keys and Secrets Management" (planned-coverage stub: `.env`, HF/OpenAI/Anthropic env vars, keyring, Colab Secrets, Codespaces, cloud secret managers, CI/CD secrets, leak detection). I.5 next-link updated to point at the new I.6. The I-index lists all eight sections.

## Notes on linter behavior

A code formatter ran during the edits and (a) dropped the chapter-letter prefix from `<h1>` headings (e.g. `H.1 Essential Libraries` to `Essential Libraries`), and (b) updated some What-Comes-Next text. Edits were reapplied as needed.

## Items flagged but not executed

- Per-section nav prev/next title prefixes that still read C/D/E/L on a handful of sections (e.g. `section-h.3.html` and `section-h.4.html` nav-title labels). Cosmetic; outside the user's enumerated items.
- `M.4.X` and `M.5.X` headings within K.4 / K.5 were not bulk-renumbered to `K.4.X` / `K.5.X`. The audit calls this out under point 9 (orthogonal cleanup) and the user's task did not specifically request it.
- No external research, no files outside H/I/J/K touched.
