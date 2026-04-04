# Building Conversational AI using LLM and Agents

A comprehensive, hands-on textbook covering modern Large Language Model technology from foundations to production deployment.

## [View the Full Syllabus](https://apartsinprojects.github.io/LLMBook/)

## Course Overview

**36 Chapters (00-35) + Capstone + 10 Appendices** covering:

| Part | Chapters | Topics |
|------|----------|--------|
| **I: Foundations** | 00-05 | ML/PyTorch basics, NLP, tokenization, attention, transformers, decoding |
| **II: Understanding LLMs** | 06-09, 18 | Pre-training, scaling laws, modern models, reasoning, inference optimization, interpretability |
| **III: Working with LLMs** | 10-12 | APIs, prompt engineering, hybrid ML+LLM architectures |
| **IV: Training & Adapting** | 13-17 | Synthetic data, fine-tuning, PEFT, distillation, alignment |
| **V: Retrieval & Conversation** | 19-21 | Embeddings, vector databases, RAG, conversational AI |
| **VI: Agentic AI** | 22-26 | AI agents, tool use and protocols, multi-agent systems, specialized agents, agent safety |
| **VII: Multimodal & Applications** | 27-28 | Multimodal models, LLM applications |
| **VIII: Evaluation & Production** | 29-31 | Evaluation, observability, monitoring, production engineering |
| **IX: Safety & Strategy** | 32-33 | Safety, ethics, regulation, LLM strategy, ROI |
| **X: Frontiers** | 34-35 | Emerging architectures, AI and society |
| **Capstone** | | End-to-end conversational AI agent project |
| **Appendices** | A-J | Math, ML, Python, setup, Git, glossary, hardware, models, prompts, benchmarks |

## Repository Structure

```
LLMBook/
├── index.html                                     # Interactive syllabus (GitHub Pages)
├── part-1-foundations/
│   ├── module-00-ml-pytorch-foundations/
│   ├── module-01-foundations-nlp-text-representation/
│   ├── module-02-tokenization-subword-models/
│   ├── module-03-sequence-models-attention/
│   ├── module-04-transformer-architecture/
│   └── module-05-decoding-text-generation/
├── part-2-understanding-llms/
│   ├── module-06-pretraining-scaling-laws/
│   ├── module-07-modern-llm-landscape/
│   ├── module-08-reasoning-test-time-compute/
│   ├── module-09-inference-optimization/
│   └── module-18-interpretability/
├── part-3-working-with-llms/
│   ├── module-10-llm-apis/
│   ├── module-11-prompt-engineering/
│   └── module-12-hybrid-ml-llm/
├── part-4-training-adapting/
│   ├── module-13-synthetic-data/
│   ├── module-14-fine-tuning-fundamentals/
│   ├── module-15-peft/
│   ├── module-16-distillation-merging/
│   └── module-17-alignment-rlhf-dpo/
├── part-5-retrieval-conversation/
│   ├── module-19-embeddings-vector-db/
│   ├── module-20-rag/
│   └── module-21-conversational-ai/
├── part-6-agentic-ai/
│   ├── module-22-ai-agents/
│   ├── module-23-tool-use-protocols/
│   ├── module-24-multi-agent-systems/
│   ├── module-25-specialized-agents/
│   └── module-26-agent-safety-production/
├── part-7-multimodal-applications/
│   ├── module-27-multimodal/
│   └── module-28-llm-applications/
├── part-8-evaluation-production/
│   ├── module-29-evaluation-observability/
│   ├── module-30-observability-monitoring/
│   └── module-31-production-engineering/
├── part-9-safety-strategy/
│   ├── module-32-safety-ethics-regulation/
│   └── module-33-strategy-product-roi/
├── part-10-frontiers/
│   ├── module-34-emerging-architectures/
│   └── module-35-ai-society/
├── capstone/
└── appendices/
    ├── appendix-a-mathematical-foundations/
    ├── appendix-b-ml-essentials/
    ├── appendix-c-python-for-llm/
    ├── appendix-d-environment-setup/
    ├── appendix-e-git-collaboration/
    ├── appendix-f-glossary/
    ├── appendix-g-hardware-compute/
    ├── appendix-h-model-cards/
    ├── appendix-i-prompt-templates/
    └── appendix-j-datasets-benchmarks/
```

## How This Book Is Built

Each chapter is produced by a **42-agent AI team** orchestrated through **13 phases** ([meet the team](https://apartsinprojects.github.io/LLMBook/front-matter/section-fm.7.html)):

1. **Setup**: Chapter Lead defines scope, outline, and coordination plan
2. **Planning**: Curriculum alignment, deep explanation design, teaching flow review
3. **Content Building**: Examples and analogies, code pedagogy, visual learning, exercises
4. **Structural Review**: Book-level organization and coherence
5. **Self-Containment**: Prerequisite availability verification
6. **Engagement & Memorability**: Title/hook design, first-page conversion, aha-moments, project catalysts, demos, mnemonics
7. **Writing Clarity**: Plain-language rewriting, sentence flow, jargon gating, micro-chunking, fatigue detection
8. **Learning Quality Review**: Student advocate, cognitive load optimizer, misconception analyst, research scientist
9. **Integrity Check**: Fact checker, terminology keeper, cross-reference architect
10. **Visual Identity**: Brand consistency across all figures and callouts
11. **Final Polish**: Narrative continuity, style/voice, engagement, senior developmental editor
12. **Frontier & Currency**: Research frontier mapping, content update scouting
13. **Quality Challenge**: Skeptical reader challenges distinctiveness and quality

## Target Audience

Software engineers with Python experience who want to build production LLM applications. Assumes basic linear algebra and probability; all other prerequisites are covered in the appendices.

## License

All rights reserved. This material is for educational use.
