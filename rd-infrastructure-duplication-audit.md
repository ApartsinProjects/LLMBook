# R&D Infrastructure Duplication Audit (post-v9)

Scope: Appendix H (Python for LLM), Appendix I (Environment Setup), Appendix J (Git/DVC/Reproducibility), Appendix K (Experiment Tracking). Target: every version-control concept lives only in J; every experiment-tracking concept lives only in K (with J cross-reference for git-tag-per-run).

## Summary
- Total Git / version-control references found outside J: **9** (1 in H, 2 in I, 6 in K)
- Sections needing consolidation: **3** (K.4 GitHub Actions, K.2 MLflow Projects from Git, J.3 vs K.1/K.2 experiment tracking)
- Sections needing deletion or major trim: **2** (J.3 entire section, J.4 `git commit hash` reference plus minor mention of `requirements.txt`/seeds left as-is)
- Most serious overlap: **K.1+K.2 vs J.3** — three full appendices teach W&B init/log and MLflow log_param/log_metric. K.4 also independently re-introduces a Git-driven CI/CD model deploy pattern.

## Current topic spread (where each concept appears today)

| Topic | H | I | J | K |
|---|---|---|---|---|
| Python core libs (transformers, torch, pandas) | ✅ H.1 | small dup I.4 | — | — |
| Virtual env / venv / conda / uv / pixi | ✅ H.2 | ⚠ dup I.3 | — | — |
| Jupyter / Colab | ✅ H.3 | small dup I.5 | — | — |
| LLM scripting patterns (chat templates, retries, checkpoints) | ✅ H.4 | — | — | — |
| Hardware (GPU/VRAM/disk) | — | ✅ I.1 | — | — |
| CUDA driver install | — | ✅ I.2 | — | — |
| Cloud providers (AWS/GCP/Colab/RunPod) | — | ✅ I.5 | — | — |
| Setup verification script | — | ✅ I.6 | — | — |
| API key / secrets management | mention H.3 (Colab Secrets) | mention I.5 (HF_TOKEN, Colab Secrets) | — | — |
| `.gitignore` | — | — | ✅ J.1 | — |
| Git LFS for model files | — | — | ✅ J.1 | — |
| Branching strategy | — | — | ✅ J.1 | — |
| DVC | — | — | ✅ J.2 | — |
| `dvc.yaml` pipelines / `dvc repro` / `git tag` baseline | — | — | ✅ J.2 | — |
| Random seeds / `requirements.txt` for reproducibility | ⚠ H.2 ("reproducibility" word only) | ⚠ I.3 "Version Pinning" callout | ✅ J.4 | — |
| Hardware metadata capture (CUDA, torch versions) | — | small overlap I.6 verify_setup.py | ✅ J.4 | — |
| `git commit hash` in experiment logs | — | — | ✅ J.4 | — |
| W&B `init` / `log` / config | mini snippet H.1 (libraries table) | mini snippet I.4 install | ⚠ J.3 (full example) | ✅ K.1 (canonical) |
| MLflow `start_run` / `log_param` / `log_metric` | — | mini snippet I.4 install | ⚠ J.3 (full example) | ✅ K.2 (canonical) |
| MLflow Projects from Git repo | — | — | — | ⚠ K.2 (Git URL embedded) |
| GitHub Actions CI/CD deploy | — | — | — | ⚠ K.4 (full YAML) |
| Model versioning / aliases / registry | — | — | — | ✅ K.4 |
| Hyperparameter sweeps / Optuna | — | — | — | ✅ K.1, K.3 |
| Evaluation dashboards / observability | — | — | — | ✅ K.5 |

Legend: ✅ canonical home, ⚠ duplicate or out-of-scope mention, small dup = brief code line, — absent.

## Per-appendix audit

### Appendix H: Python for LLM

**Current sections**
- H.1 Essential Libraries (transformers, torch, numpy/pandas, plus a table that briefly mentions `wandb`, `langchain`, `peft`, `trl`, `sentence-transformers`)
- H.2 Virtual Environments and Dependency Management (venv, conda, uv)
- H.3 Jupyter Notebooks and Google Colab
- H.4 Common Patterns for LLM Scripting (model loading, chat templates, DataLoader, API retry, checkpoint save/load + push_to_hub)

**Duplications found**
1. `index.html` line 47: `For version control and experiment tracking on top of this Python foundation, see Appendix J (Git and Collaboration).` This is a clean cross-reference, **not** a duplication; preserve.
2. H.2 lines 32, 47, 52: the word "reproducibility" appears three times (as the justification for using `pip freeze`/`requirements.txt`). This is the right scope (reproducibility-of-environment is a property of dependency management) but the phrase **overlaps in tone** with J.4's reproducibility checklist. Action: keep H.2's reproducibility wording (it is about environments, not experiments), but ensure J.4 owns the broader checklist.
3. H.1 includes mini `wandb.init/log/finish` example. This duplicates K.1. Action: replace the wandb code in H.1 with a one-line install reference and pointer to K.1.

**Recommended restructure**
- Keep H exactly as scoped: language-level Python only. Strip the `wandb.init/log/finish` mini-example from H.1 (lines ~286-295) and replace with a one-sentence pointer to K.1.
- Move the Colab "Secrets management" tip from H.3 to a new I.7 (API Key Management) where it belongs alongside HF_HOME and `HF_TOKEN`.

### Appendix I: Environment Setup

**Current sections**
- I.1 Hardware Requirements (VRAM table, RAM, disk, HF cache location)
- I.2 CUDA and Driver Setup
- I.3 Python Environment Setup (conda, venv + pip)
- I.4 Installing Key Libraries (full pip-install recipe, per-part shopping list)
- I.5 Cloud Options (Colab/Lambda/RunPod/AWS/GCP/Modal/Vast.ai + Colab Quick Start)
- I.6 Verifying Your Setup (verify_setup.py + Setup Checklist)

**Duplications found**
1. I.3 entire section duplicates H.2. Both create venv and conda envs with the same commands.
   - I.3 lines 39-50 (`conda create -n llm python=3.11 …`) duplicates H.2 lines 55-66.
   - I.3 lines 44-50 (`python -m venv llm-env …`) duplicates H.2 lines 35-51.
   - I.3 Code Fragment I.3.2 (lines 55-63) duplicates H.2 Code Fragment H.2.1.
2. I.4 lines 33-52 (pip install transformers/peft/trl/wandb/mlflow) overlaps with H.1's library table. Different angle, but the lists overlap.
3. I.5 Colab Quick Start (lines 92-101) duplicates H.3's Colab tips list (lines 45-51).
4. I.6 verify_setup.py (lines 33-86) captures `torch.cuda.get_device_name`, `torch.version.cuda`, `torch.__version__`. The reproducibility section J.4 (Code Fragment J.4.2) captures **the same fields** as `config` dict for experiment logs. The overlap is intentional and small; preserve both.
5. The "What Comes Next" footer of I.6 already cleanly hands off to J.

**Git mentions in I (the only two)**
- I.6 line 153: `<a href="../appendix-j-git-collaboration/index.html">Appendix J: Git, DVC, and Reproducibility</a>` — clean nav, preserve.
- I.6 line 158: same link in `<nav class="chapter-nav">`. Preserve.

There is **no actual Git content** in Appendix I. The flag "Git appears in several places" refers to navigational link text, not duplicated body content. Acceptable as-is.

**Recommended restructure**
- Rename I.3 to **"Linking CUDA to PyTorch (pip wheels and conda channels)"** and trim it to the CUDA-specific concern. Drop the duplicate venv/conda recipes and direct readers to H.2.
- Merge I.5 Colab Quick Start into H.3 Colab section, or leave it focused on cloud-instance bootstrap (Colab cell sequence + Drive mount) while H.3 handles notebooks generally.
- Add **I.7 API Keys and Secrets** absorbing the scattered Colab Secrets / HF_TOKEN tips. Currently no canonical home.

### Appendix J: Git/DVC

**Current sections**
- J.1 Git Basics for ML Projects (.gitignore template, Git LFS, branching strategy)
- J.2 Data Version Control (DVC) (`dvc add`, `dvc.yaml`, `dvc repro`, `git tag v1.0-baseline`)
- J.3 Experiment Tracking (W&B + MLflow + feature comparison table) — **this fully overlaps Appendix K**
- J.4 Reproducibility Best Practices (checklist, seeds, hardware metadata, "git commit hash" mentioned in checklist item 4)

**Topic overlap with K**
- J.3 contains a `wandb.init`+`Trainer` example (lines 35-59) which is a strict subset of K.1 sections 2-3.
- J.3 contains an `mlflow.set_experiment`+`log_params`+`log_metrics`+`log_artifact` example (lines 62-83) which is a strict subset of K.2 sections 2-3.
- J.3 contains a "W&B vs MLflow" comparison table (lines 85-118) that overlaps with the index of K (lines 38-39 narrative description).

**Missing topics to absorb from H/I/K**
- A short "git commit hash + experiment ID linkage" recipe (currently scattered: J.4 mentions logging it, K never explicitly shows how). Should become a new sub-section in J.4 or J.1.
- GitHub Actions CI/CD for ML deploys (currently sits in K.4 lines 201-259). This is **deployment plumbing**; it belongs with collaboration/MLOps in J, not in K.
- The MLflow-Projects-from-Git pattern (K.2 lines 141-168) — a Git invocation. Move the Git-driven invocation pattern to J and leave a cross-reference in K.2.

**Recommended restructure**
- **Delete J.3 entirely.** Replace with a short stub: `Experiment tracking is its own appendix; see Appendix K. The git-tag-per-run pattern that connects experiments to code state is below in J.4.`
- Add **J.3 (replacement): Linking Experiments to Code State** — covers `git tag` per run, `git rev-parse HEAD` injection into wandb config, `git describe --dirty` in MLflow params, and DVC `dvc exp` tagging.
- Add **J.4 (was J.4 but expanded) "Reproducibility & MLOps Patterns"** — keep the existing seeds/hardware/config checklist. Absorb the GitHub Actions YAML from K.4. Note: J.4's last-line "Continue to Appendix K: Glossary" is wrong (J is followed by K = Experiment Tracking now). Fix this stale forward-link.
- **Should become** the single home for: Git basics, LFS, branching, DVC, `dvc.yaml`, `git tag`, GitHub workflows, reproducibility checklist, random-seed recipes.

### Appendix K: Experiment Tracking

**Current sections**
- K.1 Weights and Biases: Runs, Logging, and Sweeps
- K.2 MLflow: Tracking, Projects, and Model Registry
- K.3 Experiment Comparison and Hyperparameter Optimization
- K.4 Model Registry and Deployment Workflows
- K.5 LLM Evaluation Dashboards and Observability

**Duplications found**
1. K.1 lines 38-44 install + login snippet duplicates I.4 line 46 (`pip install wandb mlflow`). Acceptable: the install is one line and the auth flow is unique here.
2. K.2 section 5 "MLflow Projects: Reproducible Packaging" (lines 139-168) introduces a Git URL (`https://github.com/myorg/llm-finetuning`) and discusses "any Git repository" — **Git-driven invocation pattern**. This is the strongest cross-appendix Git mention in K.
3. K.4 section M.4.6 "CI/CD Integration" (lines 199-259) is a full GitHub Actions YAML for model deployment. **Belongs in J (MLOps) not K (tracking)**.
4. K.4 section M.4.7 "LLM-Specific Registry Considerations" uses the word "versioning" 4 times. This is registry/tracking versioning (not VC versioning) — preserve.
5. K.4 line 111 inline cross-reference to Appendix P (inference serving) is appropriate.
6. K.5 — clean, no Git content, no VC content. Pure W&B/MLflow evaluation dashboards.

**Recommended restructure**
- K.1, K.3, K.5: leave as-is.
- K.2: trim the "MLflow Projects" section (M.5/section 5) to a 1-paragraph summary. Move the GitHub-URL example and the "any Git repository" prose to a new J sub-section. Replace with: `MLflow Projects can be run from a local path or a Git repo; see Appendix J for the Git invocation pattern and CI/CD wiring.`
- K.4: extract section M.4.6 (CI/CD Integration) entirely. Move to **J.4** (or new J.5). Replace with a single paragraph: `Validation gates plug into your CI/CD pipeline; see Appendix J Section J.4 for the GitHub Actions wiring.`
- Add a `What Comes Next` footer on K.5 pointing forward (currently incomplete).

## Proposed final section list

```
H Python:
  H.1 Essential Libraries (numpy/pandas/torch/transformers; drop wandb mini-example)
  H.2 Virtual Environments (venv/conda/uv/pixi; mention reproducibility re: deps only)
  H.3 Jupyter and Google Colab
  H.4 Common Patterns for LLM Scripting

I Env:
  I.1 Hardware Requirements (GPU/VRAM/disk)
  I.2 CUDA and Driver Setup
  I.3 Linking CUDA to PyTorch (cu124 wheels, conda pytorch-cuda; NOT duplicate venv steps)
  I.4 Installing the LLM Library Stack (single canonical pip-install recipe)
  I.5 Cloud Options (Colab/Lambda/RunPod/AWS/GCP/Modal/Vast.ai + bootstrap)
  I.6 IDE Setup and Editor Integrations (VS Code, Cursor, Codespaces, Jupyter in VS Code) — NEW
  I.7 API Keys and Secrets Management (HF_TOKEN, OPENAI_API_KEY, Colab Secrets, .env, keyring) — NEW
  I.8 Verifying Your Setup

J Git/DVC:
  J.1 Git Basics for ML Projects (.gitignore, LFS, branching for experiments)
  J.2 DVC for Data and Models (dvc add, dvc.yaml pipelines, dvc exp, git-tag-per-baseline)
  J.3 Linking Experiments to Code State (git rev-parse HEAD in wandb/mlflow params; git tag per run) — NEW, REPLACES old J.3
  J.4 Reproducibility Checklist (seeds, env pinning, hardware capture, config-as-code)
  J.5 MLOps Plumbing: GitHub Workflows and Model Deploy CI/CD — NEW (absorbs K.4 section M.4.6)

K Tracking:
  K.1 Weights & Biases (runs, logging, artifacts, sweeps)
  K.2 MLflow (tracking, model registry; trim Projects-from-Git, backref J)
  K.3 Comparison & HPO (Optuna, sweep agents, statistical tests)
  K.4 Model Registry & Deployment Patterns (registry, aliases, validation gates; DROP CI/CD YAML → backref J.5)
  K.5 LLM Evaluation Dashboards & Observability
```

## Concrete migration steps (numbered)

1. **Delete** `appendix-j-git-collaboration/section-j.3.html` body content (lines 32-123). Replace with a one-paragraph stub plus a new sub-section "Linking experiments to code state": show `git rev-parse HEAD` + `wandb.config.update({"git_sha": ...})`, and `mlflow.log_param("git_sha", git_sha)`. Add a callout cross-reference: `For the full W&B / MLflow APIs see Appendix K.`

2. **Move** the GitHub Actions YAML and `validate_model.py` from `appendix-k-experiment-tracking/section-k.4.html` lines 200-259 to a new section in Appendix J (suggested J.5 "MLOps Plumbing"). In K.4 leave 1 paragraph: `Validation gates plug into CI/CD; see Appendix J Section J.5 for the GitHub Actions wiring.`

3. **Trim** `appendix-k-experiment-tracking/section-k.2.html` MLflow Projects section (lines 139-169). Keep the conceptual paragraph about MLproject files; remove the Git-URL `mlflow.run("https://github.com/myorg/...")` example. Add: `For invoking MLflow Projects from a Git repository, see Appendix J Section J.5.`

4. **Trim** `appendix-h-python-for-llm/section-h.1.html` lines 286-295 (wandb mini-example in the "wandb in Practice" callout). Replace with: `See Appendix K Section K.1 for the canonical W&B logging API.` Keep the `wandb` row in the libraries table for context only.

5. **Trim** `appendix-i-environment-setup/section-i.3.html` lines 35-65. Remove the conda env creation (`conda create -n llm`) and the venv creation (`python -m venv llm-env`) duplicates. Replace with: `Set up your virtual environment per Appendix H Section H.2, then proceed with the CUDA-specific PyTorch wheel installation below.` Keep only the `pip install torch --index-url …/cu124` and `conda install pytorch pytorch-cuda=12.4` parts that are CUDA-specific.

6. **Move** the Colab Secrets paragraph from H.3 line 49 and the HF_HOME callout from I.1 lines 80-83 to a new section **I.7 "API Keys and Secrets Management"**. Add `.env` / `python-dotenv`, `keyring`, and the GitHub Codespaces secrets pattern.

7. **Fix** the stale forward-link in `appendix-j-git-collaboration/section-j.4.html` line 81 (`Continue to Appendix K: Glossary…`). The next appendix is K = Experiment Tracking, not glossary.

8. **Fix** the `<span class="section-num">` legacy letters in the four index.html files. Currently they read C.1/D.1/E.1/L.1 (old numbering) instead of H.1/I.1/J.1/K.1. This is a separate visual bug but worth noting: `appendix-h-python-for-llm/index.html` lines 53/59/65/71; `appendix-i-environment-setup/index.html` lines 53/59/65/71/77/83; `appendix-j-git-collaboration/index.html` lines 53/59/65/71; `appendix-k-experiment-tracking/index.html` lines 54/60/66/72/78.

9. **Renumber** the H1 headings within section files to match the appendix letter. Examples of mismatch: `section-h.1.html` line 28 says `C.1 Essential Libraries`; `section-i.1.html` line 25 says `D.1 Hardware Requirements`; `section-j.1.html` line 28 says `E.1 Git Basics for ML Projects`; `section-k.1.html` line 28 says `L.1 Weights and Biases…`. Update the in-page heading and `code-caption` labels.

10. **Add** an explicit cross-reference callout at the top of K.1 and K.2: `Prerequisite: Appendix J Section J.1 (.gitignore, branching). Every example here assumes your repo is already under version control.`

## Boundary statements (insert into each appendix's "Big Picture" callout)

- **H scope:** "Python language and libraries for LLM work. Excludes: machine setup (see I), version control (see J), experiment platforms (see K)."
- **I scope:** "Hardware, drivers, and infrastructure-level setup. Excludes: Python libraries (see H), version control (see J)."
- **J scope:** "All version-control concerns for ML: Git, LFS, DVC, branching strategy, git-tag-per-experiment, reproducibility checklists, and the CI/CD plumbing that ties code commits to model deploys."
- **K scope:** "Experiment-tracking platforms (W&B, MLflow) and what they uniquely provide: runs, sweeps, model registry, evaluation dashboards. For the Git/DVC pieces that link these tools to code state, see J."

## Key findings (TL;DR)

- "Git appears in several places" is true mostly in K: K.2 (MLflow Projects from a Git URL), K.4 (GitHub Actions deploy YAML), plus implicit references via "versioning" terminology. Appendix I has only nav-link mentions, which are acceptable.
- The biggest duplication is **not** Git but **experiment tracking**: J.3 fully duplicates K.1+K.2 at smaller scale. J.3 should be deleted and replaced with the missing "git-tag-per-run" recipe.
- Appendix H is mostly clean; only a token `wandb.init` snippet sneaks in.
- Appendix I has duplicate venv/conda recipes overlapping H.2 (I.3 should be CUDA-only).
- Two stale forward-links exist (I.6 fine, J.4 wrong "Glossary" link).
- Section numbering in headings and section cards uses **old letters** (C/D/E/L) — orthogonal cleanup needed.
