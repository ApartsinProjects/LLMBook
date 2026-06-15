# Graduate-Depth Audit: Part 10 (LLM Security & Runtime Safety)
| Section | Title (short) | Verdict | Missing piece (only if not COURSE-READY) |
|---|---|---|---|
| 47.1 | Prompt Injection & Jailbreaking | COURSE-READY | |
| 47.2 | Data Poisoning, Extraction & Jailbreaking | COURSE-READY | |
| 47.3 | Red Teaming Frameworks & Security Testing | COURSE-READY | |
| 47.4 | Supply Chain, Confidential Compute & Multimodal | COURSE-READY | |
| 48.1 | What Guardrails Are (and Are Not) | COURSE-READY | |
| 48.2 | Input Guardrails: Injection Detection & PII | COURSE-READY | |
| 48.3 | Output Guardrails (Llama Guard, NeMo, ShieldGemma) | COURSE-READY | |
| 48.4 | Policy DSLs & Constrained Decoding | COURSE-READY | |
| 48.5 | Multimodal Guardrails | COURSE-READY | |
| 49.1 | Agent Safety & Prompt Injection Defense | COURSE-READY | |
| 49.2 | Sandboxed Execution Environments | COURSE-READY | |
| 49.3 | Agentic Security Benchmarks (b3, tau-bench) | COURSE-READY | |
| 49.4 | Supply-Chain Security for Agent Sandboxes | COURSE-READY | |
| 49.4a | SLSA, CI Hardening & Model-Hub Scanning | COURSE-READY | |
| 49.5 | Why LLMs Hallucinate / Privacy & Memorization | COURSE-READY | |
| 50.1 | Privacy Attacks & Differential Privacy | COURSE-READY | |
| 50.2 | Machine Unlearning | COURSE-READY | |
| 50.3 | Federated Learning for Privacy-Preserving Training | DEPTH-GAP | Gradient-inversion attack mechanics (DLG/iDLG: how raw text is reconstructed from a shared gradient) are named and repeatedly cited as the motivating threat but never shown; the central threat that justifies the whole section is a label only. |
| 51.1 | Platforms | CATALOG-OK | |
| 51.2 | Libraries & Frameworks | CATALOG-OK | |
| 51.3 | Datasets & Benchmarks | CATALOG-OK | |
| 51.4 | Models | CATALOG-OK | |
| 51.5 | External Reading & Communities | CATALOG-OK | |

## Summary
- COURSE-READY: 17 | DEPTH-GAP: 1 | NOT-SELF-CONTAINED: 0 | CATALOG-OK: 5
- Top sections most worth enriching:
  1. 50.3 Federated Learning (DEPTH-GAP): add a worked gradient-inversion trace (DLG/iDLG: optimize dummy inputs to match an observed gradient, recovering training text) so the threat that motivates secure aggregation and DP-FL is demonstrated, not just named.
  2. 48.5 Multimodal Guardrails (already COURSE-READY, marginal): the strongest add would be a concrete worked adversarial-perturbation example (frequency-domain signature plus the JPEG-defeats-it trace) rather than prose; current treatment of perturbation detection is the thinnest mechanism in an otherwise strong section.
  3. 49.3 Agentic Benchmarks (already COURSE-READY): could add one fully scored end-to-end b3 trace (a single compromised-tool scenario run with the four metrics computed) to anchor the harness code in a concrete attack/defense walkthrough.
