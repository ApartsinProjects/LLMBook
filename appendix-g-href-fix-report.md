# Appendix G Href Fix Report

**File:** `appendices/appendix-g-problem-solution-key/index.html`
**Validation:** All 109 unique `href` targets now resolve to files that exist on disk.

## Summary

- **Hrefs rewritten:** 84 (across 47 table rows, all 9 categories).
- **Hrefs stripped to plain text:** 4 (no current target exists).
- **Hrefs flagged for manual review:** 0.

## Module slug remapping (where href targets moved)

| Old (broken) | New (current) |
| --- | --- |
| `module-25-agent-safety-production/section-25.1.html` | `module-38-agent-safety-security/section-38.1.html` |
| `module-25-agent-safety-production/section-25.2.html` | `module-38-agent-safety-security/section-38.2.html` |
| `module-25-agent-safety-production/section-25.3.html` (Agent Cost Control) | `module-49-post-launch-monitoring/section-49.1.html` |
| `module-27-llm-applications/section-27.1.html` (Vibe-Coding) | `module-43-vibe-coding/section-43.2.html` |
| `module-27-llm-applications/section-27.2.html` (Finance) | `module-52-finance-llms/index.html` |
| `module-27-llm-applications/section-27.3.html` (Healthcare) | `module-53-healthcare-llms/index.html` and `section-53.7.html` |
| `module-27-llm-applications/section-27.4.html` (Legal) | `module-51-legal-llms/index.html` |
| `module-27-llm-applications/section-27.4.html` (Recommendation) | `module-59-recommendation-search/section-59.1.html` |
| `module-27-llm-applications/section-27.5.html` (Cybersecurity) | `module-55-cybersecurity-llms/index.html` |
| `module-27-llm-applications/section-27.6.html` (Education) | `module-54-education-llms/index.html` |
| `module-27-llm-applications/section-27.7.html` (Robotics) | `module-31-multimodal/section-31.6.html` |
| `module-31-strategy-product-roi/section-31.3.html` (ROI) | `module-47-scaling-economics/section-47.1.html` |
| `module-31-strategy-product-roi/section-31.4.html` (Vendor Eval) | `module-42-strategy-prioritization/section-42.2.html` and `42.4.html` |
| `module-31-strategy-product-roi/section-31.5.html` (Compute Planning) | `module-46-compute-planning/section-46.3.html` and `module-47-scaling-economics/section-47.2.html` |
| `appendix-e-prompt-templates` | `appendix-d-langchain` (LangChain prompt templates) |
| `appendix-c-huggingface-ecosystem` (DSPy label) | `appendix-e-orchestration-frameworks` (DSPy/LlamaIndex live here) |
| `appendix-d-langchain` (LlamaIndex label) | `appendix-e-orchestration-frameworks` |

## Hrefs stripped to plain text (no current target)

1. `appendix-k-datasets-benchmarks` (Benchmarks label, row: LLM evaluation and benchmarking) — kept text "Benchmarks".
2. `appendix-k-datasets-benchmarks` (Datasets label, row: Data curation and filtering) — kept text "Datasets".
3. `appendix-k-hardware-compute` (Hardware Guide, row: Hardware planning) — repointed Tools col to `appendix-m-distributed-ml`.
4. `appendix-d-model-cards` (Model Cards, row: Regulatory compliance) — kept text "Model Cards".

## Display-label updates

Beyond href fixes, all stale chapter.section display numbers were aligned with the current chapter numbering (chapter number = module number). Examples: `12.1 → 14.1`, `13.x → 15.x`, `15.x → 18.x`, `16.x → 19.x`, `17.x → 20.x`, `18.x → 22.x`, `19.x → 23.x`, `20.x → 24.x`, `21.x → 26.x`, `22.x → 27.x`, `23.x → 28.x`, `24.x → 29.x`, `26.x → 31.x`, `28.x → 34.x`, `29.x → 35.x`, `30.x → 37.x`, `31.x → 42.x/46.x/47.x`, `25.x → 38.x`, `6.x → 7.x`, `7.x → 8.x`, `8.x → 9.x`, `9.x → 10.x`, `10.x → 11.x`, `11.x → 13.x`, `13.x synth → 17.x`. Two unlinked text fragments ("Section 7.1", "Section 20.1", "Section 37.2", "Section 26.1", "layer normalization") were converted into proper `<a>` links to existing sections.
