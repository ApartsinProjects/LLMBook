"""v6.41: Fix bare "Section X.Y" placeholder text where concept names belong.

Background: a previous auto-linker pass replaced concept-name strings with
cross-reference labels but never substituted back the actual concept name.
Now bare "Section 4.1" / "Section 6.1" / "Section 8.1" appears in places
where "softmax" / "BERT" / "chain-of-thought" was intended.

Strategy: explicit per-file substitutions derived from the 6 shallow-content
audit reports. Each substitution is a unique-in-context phrase from the
broken text; no regex magic.
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

# (file_path, old_text, new_text)
FIXES = [
    # ===== Part I =====
    ('part-1-foundations/module-00-ml-pytorch-foundations/section-0.1.html',
     'Section 4.1 Loss',
     'Cross-Entropy Loss'),

    ('part-1-foundations/module-00-ml-pytorch-foundations/section-0.2.html',
     '<strong>Section 4.1</strong>',
     '<strong>Softmax</strong>'),

    ('part-1-foundations/module-00-ml-pytorch-foundations/section-0.2.html',
     'consider <a href="../../part-1-foundations/module-04-transformer-architecture/section-4.1.html">Section 4.1</a> instead',
     'consider Layer Normalization instead'),

    ('part-1-foundations/module-00-ml-pytorch-foundations/section-0.2.html',
     'consider Section 4.1 instead',
     'consider Layer Normalization instead'),

    ('part-1-foundations/module-00-ml-pytorch-foundations/section-0.2.html',
     'class-weighted Section 4.1 loss',
     'class-weighted cross-entropy loss'),

    ('part-1-foundations/module-00-ml-pytorch-foundations/section-0.2.html',
     'class-weighted <a href="../../part-1-foundations/module-04-transformer-architecture/section-4.1.html">Section 4.1</a> loss',
     'class-weighted cross-entropy loss'),

    # ===== Part I — module 04 (Transformer Architecture) =====
    ('part-1-foundations/module-04-transformer-architecture/section-4.3.html',
     'dominant Section 4.1 in modern LLMs',
     'dominant positional encoding scheme in modern LLMs'),

    ('part-1-foundations/module-04-transformer-architecture/section-4.3.html',
     'information propagates through Section 4.1 across layers',
     'information propagates through attention layers'),

    ('part-1-foundations/module-04-transformer-architecture/section-4.3.html',
     'replaces the Section 4.1 kernel',
     'replaces the softmax kernel'),

    ('part-1-foundations/module-04-transformer-architecture/section-4.3.html',
     'With standard Section 4.1 and many heads',
     'With standard multi-head attention and many heads'),

    ('part-1-foundations/module-04-transformer-architecture/section-4.3.html',
     'Section 6.1 (Devlin et al., 2018)',
     'BERT (Devlin et al., 2018)'),

    ('part-1-foundations/module-04-transformer-architecture/section-4.4.html',
     '<td>Section 4.1</td>',
     '<td>Softmax</td>'),

    # ===== Parts II + III =====
    ('part-2-understanding-llms/module-07-modern-llm-landscape/section-7.1.html',
     'extended Section 8.1 at inference time',
     'extended chain-of-thought reasoning at inference time'),

    ('part-3-working-with-llms/module-10-llm-apis/section-10.1.html',
     'Temperature scales the logits before Section 4.1',
     'Temperature scales the logits before the softmax operation'),

    ('part-3-working-with-llms/module-10-llm-apis/section-10.1.html',
     'Built-in Section 8.1 reasoning',
     'Built-in chain-of-thought reasoning'),

    ('part-3-working-with-llms/module-10-llm-apis/section-10.4.html',
     'running its own Section 8.1 automatically',
     'running its own chain-of-thought trace automatically'),

    ('part-3-working-with-llms/module-10-llm-apis/section-10.4.html',
     'an internal Section 8.1 (the "thinking" tokens)',
     'an internal scratchpad of reasoning tokens'),

    ('part-3-working-with-llms/module-11-prompt-engineering/section-11.1.html',
     'trying Section 8.1 prompting',
     'trying chain-of-thought prompting'),

    ('part-3-working-with-llms/module-11-prompt-engineering/section-11.3.html',
     'basic and Section 8.1 prompting',
     'basic and chain-of-thought prompting'),

    ('part-3-working-with-llms/module-12-hybrid-ml-llm/section-12.2.html',
     'Section 4.1 library',
     'sentence-transformers library'),

    ('part-3-working-with-llms/module-12-hybrid-ml-llm/section-12.5.html',
     'Section 4.1 models',
     'transformer-based models (en_core_web_trf)'),

    ('part-3-working-with-llms/module-12-hybrid-ml-llm/section-12.5.html',
     'Section 32.2 risk',
     'Hallucination risk'),

    # After v6.40 renumber, "Section 32.2 risk" became "Section 29.2 risk"
    ('part-3-working-with-llms/module-12-hybrid-ml-llm/section-12.5.html',
     '<strong>Section 29.2 risk</strong>',
     '<strong>Hallucination risk</strong>'),

    # section-7.1 bib annotation
    ('part-2-understanding-llms/module-07-modern-llm-landscape/section-7.1.html',
     "OpenAI's announcement of o1's Section 8.1 reasoning capabilities",
     "OpenAI's announcement of o1's chain-of-thought reasoning capabilities"),

    # section-0.2 inside an unrelated paragraph
    ('part-1-foundations/module-00-ml-pytorch-foundations/section-0.2.html',
     "where Section 8.1 reasoning extends a Transformer's computational depth",
     "where chain-of-thought reasoning extends a Transformer's computational depth"),

    # section-4.3 attention-layer reference (multiline match issue: " Section 4.1 across layers")
    ('part-1-foundations/module-04-transformer-architecture/section-4.3.html',
     ' Section 4.1 across layers,',
     ' attention layers,'),

    # section-7.1 bib (different wording around o1)
    ('part-2-understanding-llms/module-07-modern-llm-landscape/section-7.1.html',
     "extended deliberation at inference time. Important context for the shift toward test-time compute scaling.",
     "extended deliberation at inference time. Important context for the shift toward test-time compute scaling."),  # no-op pattern just to keep entry; actual fix above

    # ===== Parts V + VI (after renumber) =====
    # Old section-22.3 is now section-20.3 (Ch 22 -> 20)
    ('part-6-agentic-ai/module-20-ai-agents/section-20.3.html',
     'internal Section 8.1 that is hidden from the user',
     'internal chain of thought (Section 8.1) that is hidden from the user'),

    # Old section-17.1 is now section-17.1 (no change for ch 17 in part-5: was 19, now 17)
    # Wait: "Section 17.1" embeddings was old chapter 19, now chapter 17.
    # So path is part-5-retrieval-conversation/module-17-embeddings-vector-db/section-17.1.html
    ('part-5-retrieval-conversation/module-17-embeddings-vector-db/section-17.1.html',
     'models like Section 4.1',
     'transformer-based models like BERT'),

    # ===== Parts IX + X + XI =====
    # Old module-29-evaluation-observability is now module-27 (Ch 29 -> 27)
    # So old section-29.2 prereq is now in section-27.2.html
    ('part-8-evaluation-production/module-27-evaluation-observability/section-27.2.html',
     'the Section 27.1 are essential',
     'the evaluation metrics from Section 27.1 are essential'),

    ('part-8-evaluation-production/module-27-evaluation-observability/section-27.4.html',
     'the Section 27.6 that support compliance monitoring',
     'the audit tooling in Section 27.6 that supports compliance monitoring'),

    # Old section-30.x = strategy-product-roi, was Ch 33, now Ch 30
    # Path: part-9-safety-strategy/module-30-strategy-product-roi/
    ('part-9-safety-strategy/module-30-strategy-product-roi/section-30.1.html',
     'Strategy without execution is a Section 29.2',
     'Strategy without execution is a hallucination'),

    ('part-9-safety-strategy/module-30-strategy-product-roi/section-30.2.html',
     'the Section 27.1 that define product success metrics',
     'the evaluation metrics from Section 27.1 that define product success'),

    ('part-9-safety-strategy/module-30-strategy-product-roi/section-30.2.html',
     'Section 29.2 risk',
     'hallucination risk'),

    ('part-9-safety-strategy/module-30-strategy-product-roi/section-30.3.html',
     'the Section 27.1 that measure LLM quality',
     'the evaluation metrics from Section 27.1'),

    ('part-9-safety-strategy/module-30-strategy-product-roi/section-30.3.html',
     'the Section 9.1 that directly affect cost calculations',
     'the inference optimization techniques from Section 9.1'),

    ('part-9-safety-strategy/module-30-strategy-product-roi/section-30.5.html',
     'the Section 9.1 that reduce hardware requirements',
     'the inference optimization techniques from Section 9.1'),
]


def main() -> int:
    fixed_files = set()
    fixed_count = 0
    misses = []
    for rel, old, new in FIXES:
        p = ROOT / rel
        if not p.exists():
            misses.append(f'  FILE NOT FOUND: {rel}')
            continue
        text = p.read_text(encoding='utf-8')
        if old not in text:
            misses.append(f'  PATTERN NOT FOUND in {rel}: {old[:60]}...')
            continue
        new_text = text.replace(old, new)
        p.write_text(new_text, encoding='utf-8')
        fixed_files.add(rel)
        fixed_count += 1

    print(f'Applied {fixed_count} substitutions across {len(fixed_files)} files.')
    if misses:
        print(f'\n{len(misses)} patterns not found (may have been renumbered or already fixed):')
        for m in misses[:25]:
            print(m)
    return 0


if __name__ == '__main__':
    sys.exit(main())
