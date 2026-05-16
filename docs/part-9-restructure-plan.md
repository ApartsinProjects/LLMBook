# Part 9 Restructure Plan — LLM Safety, Security, Guardrails, Ethics: One Major Issue per Chapter

**Author**: Architecture planning pass, 2026-05-16
**Status**: DESIGN (read-only investigation; no files moved)
**Scope**: Restructure Part IX from 3 broad chapters into 6–10 issue-focused chapters, one per orthogonal major issue.

---

## Section A — Current State Map

### Chapter 39 — Safety, Ethics & Regulation (12 sections, ~61,314 words)

| Sec | Title | Words | Dominant issue family | Destination |
|-----|-------|------:|------------------------|-------------|
| 39.1 | LLM Security Threats | 12,002 | Adversarial security (OWASP, prompt injection, jailbreak, data poisoning, extraction, supply chain, provenance) | **Split**: A1 Adversarial; A4 Privacy (PII); A2 Supply chain; A8 Watermarking; A4 Privacy (TEE) |
| 39.2 | Hallucinations | 4,628 | Truthfulness/hallucination + buried privacy | **Split**: A6 Hallucination; A4 Privacy (memorization) |
| 39.3 | Bias, Fairness & Ethics | 6,720 | Bias & fairness + cross-cultural + model cards | **Split**: A5 Bias; A9 Documentation (model cards); A5 sub (pluralistic alignment) |
| 39.4 | Regulation & Compliance | 2,909 | Regulation (EU AI Act, GDPR, sector regs) | A7 Regulation |
| 39.5 | LLM Risk Governance & Audit | 1,950 | Governance & audit | A7 Regulation (governance section) |
| 39.6 | LLM Licensing, IP & Privacy | 1,519 | IP/licensing + privacy hybrid | **Split**: A7 (licensing); A4 (DP for training) |
| 39.7 | Machine Unlearning | 3,483 | Privacy + alignment | A4 Privacy |
| 39.8 | Red Teaming Frameworks | 5,651 | Adversarial security | A1 Adversarial |
| 39.9 | EU AI Act Compliance in Practice | 5,882 | Regulation | A7 Regulation |
| 39.10 | Environmental Impact & Green AI | 5,487 | Environmental impact | A10 Environmental (own chapter) |
| 39.11 | Privacy Attacks & DP for LLMs | 7,045 | Privacy | A4 Privacy (core chapter content) |
| 39.12 | AI Governance & Open Problems | 4,038 | Governance & frontier | **Split**: A7 (governance); A11 (frontier evals) |

### Chapter 40 — Agent Safety & Security (4 sections, ~15,257 words)

| Sec | Title | Words | Destination |
|-----|-------|------:|-------------|
| 40.1 | Agent Safety & Prompt Injection Defense | 3,114 | **Split**: A3 (threat model); A2 (guardrails) |
| 40.2 | Sandboxed Execution Environments | 2,782 | A3 Agent Safety |
| 40.3 | Agentic Security Benchmarks | 4,232 | A3 Agent Safety |
| 40.4 | Supply-Chain Security for Agent Sandboxes | 5,129 | A3 + cross-link A1 |

### Chapter 41 — Tools of the Trade (5 sections, ~3,430 words)

Stays as a single closing chapter; reorganized internally by lane (Guardrails/Red-Team/Privacy/Provenance).

---

## Section B — Proposed New Part 9 Structure

**Target**: 12 chapters (11 substantive + 1 Tools).

### Chapter A1 — Adversarial Security & Red Teaming (6 sections)

1. **A1.1** OWASP Top 10 for LLMs *(from 39.1.1)*
2. **A1.2** Prompt Injection: Direct, Indirect, Multimodal *(from 39.1.2, 39.1.4, 39.1.12)*
3. **A1.3** Jailbreaks & Refusal-Bypass *(from 39.1.8 — expand with 2025-2026 taxonomy)*
4. **A1.4** Model Extraction, Stealing & Prompt Theft *(from 39.1.6)*
5. **A1.5** Automated Red Teaming: PyRIT, Garak, HarmBench *(from 39.8.1-5)*
6. **A1.6** Building an Internal Red-Team Program *(from 39.8.7, expanded)*

### Chapter A2 — Guardrails & Runtime Safety (5 sections)

1. **A2.1** What Guardrails Are (and What They Are Not) *(NEW)*
2. **A2.2** Input Guardrails: Prompt-Injection Detection & PII Pre-filtering *(NEW + 39.1.3)*
3. **A2.3** Output Guardrails: Llama Guard, NeMo Guardrails, ShieldGemma, Guardrails AI *(from 40.1.2)*
4. **A2.4** Policy DSLs & Constrained Decoding *(NEW)*
5. **A2.5** Multimodal Guardrails: Image, Audio, Video *(NEW)*

### Chapter A3 — Agent Safety & Autonomous-System Risk (6 sections)

1. **A3.1** The Agent Threat Model *(from 40.1.1)*
2. **A3.2** Sandboxed Execution: Docker, gVisor, Firecracker *(from 40.2)*
3. **A3.3** Tool-Use Safety & Least-Privilege Patterns *(NEW + 40.3.4)*
4. **A3.4** Agentic Security Benchmarks: b3, tau-bench *(from 40.3.1-5)*
5. **A3.5** Supply-Chain Security for Agent Sandboxes *(from 40.4)*
6. **A3.6** Kill-Switches & Shutdown Protocols *(NEW)*

### Chapter A4 — Privacy & Data Protection (6 sections)

1. **A4.1** Memorization: How LLMs Leak Training Data *(from 39.2.5 + 39.11.1)*
2. **A4.2** Privacy Attacks: Extraction, Membership Inference, Reconstruction *(from 39.11.1-2)*
3. **A4.3** Differential Privacy for LLM Training (DP-SGD with Opacus) *(from 39.11.3, 39.6.2)*
4. **A4.4** Federated Learning *(from 39.11.4)*
5. **A4.5** Machine Unlearning *(from 39.7)*
6. **A4.6** PII Redaction & Confidential Inference (TEEs) *(from 39.1.3, 39.1.10, 39.11.4)*

### Chapter A5 — Bias, Fairness & Disparate Impact (5 sections)

1. **A5.1** Sources of Bias *(from 39.3.1)*
2. **A5.2** Measuring Bias: Group, Intersectional, Behavioral *(from 39.3.2)*
3. **A5.3** Cross-Cultural NLP & Multilingual Evaluation Gaps *(from 39.3.4)*
4. **A5.4** Pluralistic Alignment *(from 39.3.4.3-5)*
5. **A5.5** Mitigation: Data Curation, Culture-Aware RLHF, Regional Adaptation *(from 39.3.6-7)*

### Chapter A6 — Hallucination & Truthfulness (5 sections)

1. **A6.1** Hallucination Taxonomy *(from 39.2.1)*
2. **A6.2** Self-Consistency Detection & Uncertainty Estimation *(from 39.2.2)*
3. **A6.3** RAG-Based Grounding & Citation Verification *(from 39.2.3)*
4. **A6.4** Calibrated Abstention & Refusal Patterns *(NEW)*
5. **A6.5** Hallucination Evaluation Benchmarks *(NEW + cross-link Part 8 Ch 36.1)*

### Chapter A7 — Regulation, Compliance & Governance (7 sections)

1. **A7.1** Global Regulatory Landscape *(from 39.4 + 39.12.2)*
2. **A7.2** EU AI Act in Practice *(from 39.9.1-4, .7)*
3. **A7.3** GDPR for LLM Systems *(from 39.4.2)*
4. **A7.4** Sector-Specific: HIPAA, SR 11-7, NIST AI RMF, ISO 42001 *(from 39.4.3, 39.9.9)*
5. **A7.5** Risk Governance & Model Inventory *(from 39.5)*
6. **A7.6** Compliance-as-Code *(from 39.9.6, 39.9.9.4)*
7. **A7.7** Model Licensing & IP for Production Use *(from 39.6.1, 39.12.3)*

### Chapter A8 — Watermarking, Provenance & Deepfake Defense (5 sections, mostly NEW)

1. **A8.1** Why Provenance Matters *(NEW)*
2. **A8.2** Text Watermarking: Kirchenbauer, SynthID-Text *(NEW)*
3. **A8.3** Image and Video Provenance: C2PA, SynthID-Image *(from 39.1.6.1, expanded)*
4. **A8.4** Deepfake & Synthetic-Media Detection *(NEW)*
5. **A8.5** Limitations: Adversarial Watermark Removal *(NEW)*

### Chapter A9 — Transparency, Documentation, Auditability (5 sections, mostly NEW)

1. **A9.1** Model Cards *(from 39.3.3, expanded)*
2. **A9.2** Datasheets for Datasets *(from 39.3.3)*
3. **A9.3** System Cards & Frontier System Disclosures *(NEW)*
4. **A9.4** Audit Trails and Logging for Compliance *(NEW + cross-link Part 8 Ch 37)*
5. **A9.5** Explainability for High-Stakes Decisions *(NEW)*

### Chapter A10 — Environmental Impact & Sustainability (8 sections)

Intact from 39.10.1-8 (the one chapter that was already issue-focused).

### Chapter A11 — Frontier Safety & Open Problems (5 sections)

1. **A11.1** Alignment Research Frontiers *(NEW + summary of Part 4 §20.5)*
2. **A11.2** Frontier Model Evaluations: Dangerous-Capability, CBRN, Bio-Risk *(from 39.12.4 — expanded)*
3. **A11.3** Compute Governance and Frontier AI Policy *(from 39.12.1)*
4. **A11.4** Scaling Oversight, Mechanistic Interpretability & Safety Cases *(NEW — link Part 12 Ch 62)*
5. **A11.5** Open Problems in AI Safety *(from 39.12.5)*

### Chapter A12 — Tools of the Trade: Safety, Guardrails & Privacy Stack (5 sections, reorganized internally)

---

## Section C — Cross-Cutting Topics

Multiple issues span chapters. Pattern: callout boxes + cross-link, not duplication.

| Cross-cutting topic | Primary home | Cross-link callouts in |
|---------------------|--------------|-------------------------|
| Prompt injection | A1.2 / A3.1 | A2 (defense), A12 (tools), Part 3 §14.4 |
| Regulation | A7 | Every chapter gets a `regulation` sidebar |
| RLHF/Alignment | Part 4 §20 | A11.1, A5.5 |
| Hallucination eval | A6.5 + Part 8 §36.1 | bidirectional |
| PII handling | A2.2 (runtime) / A4.6 (training) | bidirectional with disambiguation |
| Red-team | A1.5-6 | A3.4, Part 8 §35.2 |
| Supply chain | A3.5 / A1.4 | bidirectional |
| Guardrails vs alignment vs eval | A2.1 sidebar "Three Layers of Safety" | every chapter opener |
| Interpretability for safety | Part 12 §62 / A11.4 | A9.5, A11.4 |

**Recommendation: NO separate "cross-cutting" chapter.** Use callouts + diagram instantiated in every chapter opener.

---

## Section D — Migration Mapping

(See plan source for full table; major moves:)

- 39.1 splits into A1.1-6 + A2.2-3 + A3.5 + A4.6 + A8.3
- 39.2 splits into A6.1-3 + A4.1-2
- 39.3 splits into A5.1-5 + A9.1-2
- 39.4 splits into A7.1, A7.3, A7.4
- 39.6 splits into A7.7 + A4.3
- 39.9 splits into A7.2 + A7.6
- 39.12 splits into A7.1, A7.7, A11.2-5
- 40.1 splits into A3.1 + A2.3
- 40.3 splits into A3.3 + A3.4

---

## Section E — Renumbering & Cascade

Part 9 grows from 3 chapters to **12 chapters** (+9 chapters).

| Part | Old Range | New Range | Delta |
|------|-----------|-----------|-------|
| 9 | 39–41 (3 ch) | 39–50 (12 ch) | +9 |
| 10 | 42–52 (11 ch) | 51–61 (11 ch) | shift +9 |
| 11 | 51–60 (10 ch) | 60–69 (10 ch) | shift +9 |
| 12 | 61–65 (5 ch) | 70–74 (5 ch) | shift +9 |

Directory renames (~13 ops):
```
module-39-safety-ethics-regulation/  -> SPLIT into module-39-adversarial-security-red-team/
                                            + module-40-guardrails-runtime-safety/
module-40-agent-safety-security/      -> module-41-agent-safety-autonomy/
                                            + module-42 through module-49 (NEW)
module-41-tools-of-the-trade/         -> module-50-tools-of-the-trade/
```

---

## Section F — Content Gaps Requiring NEW Authoring

10 net-new content blocks:

1. Jailbreak taxonomy 2025-2026 (A1.3) — expand
2. Watermarking (A8 entire chapter, mostly NEW)
3. Deepfake detection (A8.4) — zero current coverage
4. System cards (A9.3) — zero current coverage
5. Kill-switches & shutdown protocols (A3.6) — zero current coverage
6. Multimodal guardrails (A2.5) — zero current coverage
7. Calibrated abstention (A6.4) — zero current coverage
8. Frontier capability evaluations (A11.2 expanded)
9. Scaling oversight / mech-interp for safety (A11.4)
10. Policy DSLs for guardrails (A2.4) — light coverage today

### Scout sources (2026 frontier)

- AI Index Report 2026 (Stanford HAI)
- OpenAI Preparedness Framework v2, Anthropic RSP v2.0, Google FSF (2025)
- METR RE-Bench, ARC-Evals
- C2PA 2.x spec, SynthID papers
- AISI evaluation reports (UK, US AISI), MLCommons AILuminate
- 2025-2026 jailbreak papers (many-shot Anthropic, GCG, AutoDAN, PAIR)
- Llama Guard 3, ShieldGemma 2, Prompt Guard 2, Granite Guardian

---

## Section G — Risks

1. **RLHF/alignment in two parts** (P4 §20 + A11.1 + A5.5). Mitigation: explicit "for mechanics see §20" callouts; no duplicates.
2. **Hallucination in three places** (P5 RAG + P8 eval + P9 A6). Mitigation: A6 frames defense; explicit cross-link callouts.
3. **Red-team in three places** (A1 + A3.4 + P8 §35.2). Mitigation: A1 owns canonical; others reference back.
4. **PII in two chapters** (A2.2 runtime + A4.6 training). Mitigation: explicit "runtime vs training" framing.
5. **60+ inbound links to 39.1 / 39.X**. Mitigation: phase 50 cross-link script.
6. **Cognitive load**: 12 chapter cards on Part 9 index. Mitigation: cluster into 4 visual groups (Adversarial / Privacy & Bias / Compliance & Trust / Frontier).
7. **URL stability**: legacy-url-redirects.json mapping.
8. **Coordination**: must run AFTER Part 8 restructure (to avoid module-49/50/51 collisions).

---

## Section H — Migration Script Outline

Same 10-phase template as `scripts/restructure_part8/`. Create `scripts/restructure_part9/`:

```
scripts/restructure_part9/
├── 00_validate_preconditions.py
├── 10_build_migration_map.py
├── 20_move_and_rename_dirs.py
├── 30_split_sections.py        (heaviest — 5+ sections need splitting into 30+ pieces)
├── 40_rewrite_section_anchors.py
├── 50_rewrite_cross_links.py   (200-400 hrefs book-wide)
├── 60_create_new_chapter_skeletons.py (9 new chapters)
├── 70_regenerate_yaml_and_toc.py (cascade Parts 10/11/12)
├── 80_generate_redirect_map.py
├── 85_image_assets.py          (9 new chapter-opener.png via gemini-imagegen)
└── 90_verify_outcome.py
```

Estimated runtime: 60-90 seconds. Manual content phase after: author 10 net-new content blocks from Section F.

---

## Critical Files

- `book_structure.yaml`
- `toc.html`
- `part-9-safety-security-ethics/index.html`
- `part-9-safety-security-ethics/module-39-safety-ethics-regulation/section-39.1.html`
- `docs/part-8-restructure-plan.md` (precondition)
