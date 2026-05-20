# Bibliography Polish Audit Report

Date: 2026-05-20
Scope: arXiv URL backfill for `<div class="bib-ref">` and `<p class="bib-ref">` entries
across the LLMBook v2.0 branch. Restricted by the avoid-list of files actively being
edited by other agents.

## Summary

| Metric | Value |
| --- | --- |
| Files touched | 23 |
| Bibliography entries fixed | 83 |
| arXiv URLs added | 83 |
| DOIs / publisher URLs added | 0 (deferred, see Notes) |
| Author/year fixes | 0 (deferred, see Notes) |
| Final audit pass | Clean: 0 remaining bare arXiv refs, 0 malformed links in touched files |

The script that performed the polish is preserved at `scripts/polish_bib_arxiv.py`
(single-line div pattern) and `scripts/polish_bib_arxiv_v2.py` (multi-line div / p
pattern with embedded markup). Both pass over the entire tree, skip the avoid-list,
and rewrite the first bare `arXiv:NNNN.NNNNN` token inside each bib-ref to a clickable
anchor of the form:

```html
<a href="https://arxiv.org/abs/NNNN.NNNNN" rel="noopener" target="_blank">arXiv:NNNN.NNNNN</a>
```

## Files Touched

### Part 5 (VLA Models): 63 fixes across 12 files

| File | arXiv URLs added |
| --- | --- |
| `part-5-multimodal-llms/module-24-vla-models/section-24.1.html` | 6 (RT-2, OpenVLA, OXE, PaLM-E, Diffusion Policy, ALOHA Unleashed) |
| `part-5-multimodal-llms/module-24-vla-models/section-24.2.html` | 7 (OpenVLA, OXE, SigLIP, DINOv2, BridgeData V2, Llama 2, QLoRA) |
| `part-5-multimodal-llms/module-24-vla-models/section-24.3.html` | 4 (Flow Matching, Diffusion Policy, PaliGemma, OXE) |
| `part-5-multimodal-llms/module-24-vla-models/section-24.4.html` | 7 (OXE, RT-2, OpenVLA, DROID, AutoRT, Chinchilla, BridgeData V2) |
| `part-5-multimodal-llms/module-24-vla-models/section-24.5.html` | 5 (RT-2, OpenVLA, Octo, TinyVLA, LIBERO) |
| `part-5-multimodal-llms/module-24-vla-models/section-24.6.html` | 5 (OpenVLA, SimplerEnv, Domain Randomization, DROID, DIGIT) |
| `part-5-multimodal-llms/module-24-vla-models/section-24.7.html` | 6 (SayCan, Inner Monologue, Code as Policies, PaLM-E, RT-2, AutoRT) |
| `part-5-multimodal-llms/module-24-vla-models/section-24.8.html` | 5 (Code as Policies, ProgPrompt, Voyager, Toolformer, ReAct) |
| `part-5-multimodal-llms/module-24-vla-models/section-24.9.html` | 6 (VoxPoser, OWL-ViT, CLIP, Code as Policies, 3D Gaussian Splatting, Language to Rewards) |
| `part-5-multimodal-llms/module-24-vla-models/section-24.10.html` | 4 (SMART-LLM, RoCo, AutoRT, RT-2) |
| `part-5-multimodal-llms/module-24-vla-models/section-24.11.html` | 2 (Nav2 / Marathon 2, AutoRT) |
| `part-5-multimodal-llms/module-24-vla-models/section-24.12.html` | 6 (SayCan, Code as Policies, VoxPoser, OpenVLA, Inner Monologue, RT-H) |

### Part 10 (Security and Guardrails): 8 fixes across 5 files

| File | arXiv URLs added |
| --- | --- |
| `part-10-llm-security-runtime-safety/module-48-guardrails-runtime-safety/section-48.1.html` | 2 (Llama Guard, Constitutional AI) |
| `part-10-llm-security-runtime-safety/module-48-guardrails-runtime-safety/section-48.2.html` | 2 (BIPIA / Yi et al., Prompt Injection Attack / Liu et al.) |
| `part-10-llm-security-runtime-safety/module-48-guardrails-runtime-safety/section-48.3.html` | 1 (ShieldGemma) |
| `part-10-llm-security-runtime-safety/module-48-guardrails-runtime-safety/section-48.4.html` | 1 (Outlines / Willard and Louf) |
| `part-10-llm-security-runtime-safety/module-48-guardrails-runtime-safety/section-48.5.html` | 2 (Multimodal indirect injection / Bagdasaryan et al., AudioJailbreak) |

### Part 11 (Ethics, Trust, Governance): 3 fixes across 3 files

| File | arXiv URLs added |
| --- | --- |
| `part-11-llm-ethics-trust-governance/module-54-watermarking-provenance/section-54.1.html` | 1 (Generative Language Models and Automated Influence Operations) |
| `part-11-llm-ethics-trust-governance/module-54b-transparency-and-disclosure/section-54.7.html` | 1 (The Pile) |
| `part-11-llm-ethics-trust-governance/module-56-responsible-ai-tools/section-56.3.html` | 1 (HELM / Liang et al.) |

### Part 12 (Distributed Training Systems): 7 fixes across 2 files

| File | arXiv URLs added |
| --- | --- |
| `part-12-llm-systems-at-scale/module-59-distributed-training-systems/section-59.1.html` | 2 (Accurate Large Minibatch SGD / Goyal et al., Horovod / Sergeev and Del Balso) |
| `part-12-llm-systems-at-scale/module-59-distributed-training-systems/section-59.5.html` | 5 (Llama 3 Herd, OPT, PaLM, BLOOM, DeepSeek-V3) |

### Part 6 (Multi-Agent Systems): 2 fixes across 1 file

| File | arXiv URLs added |
| --- | --- |
| `part-6-agentic-ai/module-28-multi-agent-systems/section-28.3.html` | 2 (AutoGen / Wu et al., Multi-Agent Debate / Du et al.) |

## Methodology

1. Walked the repository tree, excluding `_archive/`, `KDP/`, `pagefind/`, `node_modules/`,
   `agents/`, `scripts/`, `docs/`, and the explicit avoid-list of files being edited by
   other agents (35.3, 59.2, 59.3, 59.4, 27.5, all deep-dive owned files, all mental-model
   owned files).
2. Located every `<div class="bib-ref">...</div>` and `<p class="bib-ref">...</p>` entry
   that contained an `arXiv:NNNN.NNNNN` token but no link to `arxiv.org`.
3. Used the literal arXiv ID from the citation text as the source of truth. No URL was
   fabricated; the substitution simply wraps the existing ID text in an anchor with
   `href="https://arxiv.org/abs/NNNN.NNNNN"`.
4. Re-ran an audit pass over the touched files to confirm: zero remaining bare arXiv
   references, zero malformed anchor tags, every link includes `rel="noopener"` and
   `target="_blank"`.

## Notes and Deferred Items

### Venue-only entries (33 candidates not touched)

A separate pass identified 33 entries with explicit venues (NeurIPS, ICLR, ACL, EMNLP,
ICML, CVPR, ICCV, KDD, RSS, IROS, etc.) but no arXiv ID and no link, mostly in
`part-11/module-54-watermarking-provenance/`, `part-11/module-54b-transparency-and-disclosure/`,
and `part-10/module-48-guardrails-runtime-safety/`. These were intentionally left alone
because the task constraint forbids fabricating URLs and these entries do not carry an
arXiv ID in the citation text. A future pass can resolve these by querying ACL Anthology
or the official venue proceedings, but that requires verification and was out of scope
for this run.

### Author and year normalisation (0 changes)

The task asked for normalisation of "(YYYY)" against actual publication year and
"FirstInitial. LastName" author format only when there is a clear fixable issue.
The Narayanan citation example (which should read "Narayanan et al. 2021" rather than
"Narayanan 2019") was not found in any of the touched files; the entries in the affected
files all have correct authors-with-et-al formatting and the years match the arXiv
submission years (e.g., RT-2 / 2023, OpenVLA / 2024, Llama 3 / 2024, AutoGen / 2023).
No drift was identified that met the "very high confidence" bar for editing.

### Remaining bare arXiv refs in avoid-list files

12 bib-ref entries in `section-59.2.html`, `section-59.3.html`, `section-59.4.html`, and
`section-27.5.html` still have bare arXiv IDs. These were intentionally skipped to avoid
clashing with other agents. They can be polished in a follow-up pass once those files
settle.

## Audit Pass Result

```
Touched files: 23
Total arXiv links present in bib-refs after polish: 100
Remaining bare arXiv refs (in touched files): 0
Malformed anchor tags: 0
```

All anchor tags use the canonical format `<a href="https://arxiv.org/abs/NNNN.NNNNN" rel="noopener" target="_blank">arXiv:NNNN.NNNNN</a>`.
