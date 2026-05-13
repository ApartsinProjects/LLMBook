"""10th edition Wave 7: add self-check question blocks to 15 sections
that the agent audit identified as missing them. Pre-drafted in
_agent_reports/self-checks.md.

To keep the script tractable, I include 3 questions per section in
the canonical <div class="callout self-check">...<details>...</details>
format. Each block is inserted right before the </main> closing tag
(end of section content, before chapter-nav).
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SENTINEL = '<!-- v735-self-check -->'


def block(items: list) -> str:
    """items: list of (question, answer)"""
    out = [f'<div class="callout self-check">{SENTINEL}']
    out.append('<div class="callout-title">Self-Check</div>')
    for q, a in items:
        out.append('<div class="quiz-question">' + q + '</div>')
        out.append(f'<details><summary>Show Answer</summary><div class="answer">{a}</div></details>')
    out.append('</div>')
    return '\n'.join(out) + '\n'


# Post-renumber section numbers. Each block is 3 questions covering
# recall, application, and analysis levels.
# Format: (rel_path, block_html)
INSERTIONS = [
    # Note: post-renumber, some of these section numbers shifted. I use the NEW numbers.
    # 1. ELMo / Contextual Embeddings -- Section 1.4
    ('part-1-foundations/module-01-foundations-nlp-text-representation/section-1.4.html',
     block([
        ('<strong>Q1:</strong> Word2Vec assigns "bank" the same vector in "river bank" and "investment bank." ELMo produces different vectors. What architectural choice enables this?',
         'ELMo uses a bidirectional LSTM that reads the full sentence before computing each word\'s representation. The hidden state at each position is conditioned on all surrounding tokens, so "bank" near "river" receives a representation shaped by the water-related context, while "bank" near "investment" is shaped by the financial context. Fine-tuning then specializes these context-sensitive representations for the target task with far less labeled data than training task-specific models from scratch.'),
        ('<strong>Q2:</strong> ELMo uses a weighted combination of all LSTM layers. What does each layer tend to capture, and why is the learned weighting better than always using the top layer?',
         'Lower layers capture syntactic information (POS, morphology, dependency structure); upper layers capture semantic information (word sense, coreference). NER benefits more from lower-layer syntax; coreference resolution benefits from upper-layer semantics. The task-specific learned weights let the model draw on whichever combination is most useful, rather than committing to one representation that may over-represent semantics at the expense of syntax for syntactically-sensitive tasks.'),
        ('<strong>Q3:</strong> Predict which approach is better for (a) question answering, (b) text generation: ELMo\'s bidirectional LSTM or GPT-1\'s unidirectional Transformer.',
         '(a) QA: ELMo/bidirectional wins. Understanding a question requires attending to the full question before locating the answer span; a unidirectional model cannot condition each token on future tokens. (b) Generation: GPT/unidirectional wins, and is in fact the only viable choice. Generation is autoregressive; the model must predict the next token without seeing future ones. Both predictions match practice: BERT outperformed GPT-1 on comprehension; GPT models dominate generation.'),
     ])),

    # 2. 3D Gaussian Splatting -- Section 26.7
    ('part-7-multimodal-applications/module-26-multimodal/section-26.7.html',
     block([
        ('<strong>Q1:</strong> NeRFs are slow; 3DGS is 100+ FPS. What architectural decision accounts for the speed difference, and what does 3DGS trade away?',
         'NeRFs render by casting rays and evaluating an MLP at hundreds of sample points per ray; every pixel requires thousands of neural-network forward passes. 3DGS replaces the implicit neural field with millions of explicit 3D Gaussian ellipsoids projected onto the image plane as 2D splats and composited via alpha blending using GPU rasterization hardware. Trade-offs: memory scales with scene complexity (1-5M Gaussians per scene vs. a fixed-size MLP); fine semi-transparent geometry is harder to represent; initial optimization from photographs is still gradient-based and similar cost to NeRF.'),
        ('<strong>Q2:</strong> A diffusion model generates 2D views of a scene to optimize a 3DGS representation. Why is multi-view consistency harder for generated images than for real photographs?',
         'Diffusion models generate each viewpoint independently without 3D awareness: a table that appears in one view may be missing in another; lighting can be inconsistent; geometry can contradict itself across cameras. Real photographs are projections of the same physical scene and are inherently consistent. Architectures like Zero123 and MVDiffusion address this by conditioning the diffusion model on camera pose, improving geometric consistency.'),
        ('<strong>Q3:</strong> Name two advantages of 3DGS reconstructions over traditional 3D simulation for autonomous-driving training data, and one significant limitation.',
         'Advantages: (1) Photorealism &mdash; captures real-world texture, lighting, materials with fidelity hand-authored simulators cannot match. (2) Speed of content creation &mdash; a 3DGS scene can be reconstructed from a 5-minute drive-through video in hours vs. months for traditional 3D asset creation. Limitation: 3DGS reconstructs only what was captured. Traditional simulators can generate arbitrary counterfactuals (rain at 2 AM with a child running into the road), which are essential for training perception on rare safety-critical events.'),
     ])),

    # 3. AI Gateways and Model Routing -- Section 29.5 (was 28.5)
    ('part-8-evaluation-production/module-29-production-engineering/section-29.5.html',
     block([
        ('<strong>Q1:</strong> Your app calls OpenAI directly. OpenAI has a 45-minute outage. What happens, and how would an AI gateway with failover change the outcome?',
         'Without a gateway, your service returns errors for 45 minutes. With a gateway configured for automatic failover, it detects the provider failure (via health checks or HTTP 5xx) and routes requests to a fallback provider (Anthropic Claude or a self-hosted model) without any code change in the application. The gateway absorbs provider volatility. This is the primary reliability argument for introducing a gateway layer.'),
        ('<strong>Q2:</strong> Semantic caching differs from standard HTTP response caching. Explain why, and when does it save money?',
         'HTTP caching uses exact key matching (same URL returns same cached response). Semantic caching embeds the query and finds cached responses to semantically similar queries above a similarity threshold. It saves money when queries are paraphrases ("What is RAG?" and "Can you explain retrieval-augmented generation?"). Provides no benefit for creative generation (users want novel outputs), highly varied queries unlikely to repeat, or very low-traffic endpoints where cache hit rates stay near zero.'),
        ('<strong>Q3:</strong> A team argues against using LiteLLM Proxy because "it adds latency." Evaluate the tradeoff.',
         'A co-located proxy adds 1-5ms. LLM inference takes 500ms-10s+, so overhead is under 1%. Worth paying when: managing multiple providers, needing centralized cost tracking, requiring failover without code changes, or A/B testing models without redeployment. Not worth paying when: single-provider edge deployments where the gateway cannot be co-located, or extremely latency-sensitive real-time apps (voice streaming) where 5ms matters.'),
     ])),

    # 4. Durable Execution -- Section 29.6 (was 28.6)
    ('part-8-evaluation-production/module-29-production-engineering/section-29.6.html',
     block([
        ('<strong>Q1:</strong> An agent pipeline runs 20 sequential LLM calls over 15 minutes. The server crashes at step 14. Without durable execution and with Temporal, what happens at restart?',
         'Without durability: all 14 completed steps are lost. Next invocation restarts from step 1, incurring full LLM cost again. With Temporal: workflow state is persisted to a database after each activity completes. On restart, the workflow function re-executes from the beginning, but Temporal intercepts each activity whose result is already in the event history and returns the cached result. Only step 15 (the failed step) actually re-runs against the external LLM.'),
        ('<strong>Q2:</strong> What is exactly-once semantics, and why is it critical for agent tool calls that send emails or charge credit cards?',
         'Exactly-once semantics guarantees each step executes precisely one time even across retries and crashes. Without it, a retry after a crash can re-execute a completed step, sending the email twice or charging the customer twice. Temporal implements this by replaying workflow code deterministically and returning cached activity results from the event history for already-completed steps, rather than re-invoking the actual external service. Retries become idempotent without developers writing idempotency logic in every tool.'),
        ('<strong>Q3:</strong> When would you choose application-level checkpointing over a durable execution framework like Temporal?',
         'Application-level checkpointing is appropriate for: simple workflows (under 5 steps), teams already using a database-backed state machine pattern, or avoiding the operational overhead of a Temporal cluster. Temporal/Inngest become necessary when: workflows run for minutes or hours, workflows have many parallel branches that must be joined, workflows include human-in-the-loop approval with arbitrary wait times, or cross-service fan-outs must be coordinated reliably.'),
     ])),

    # 5. Red Teaming -- Section 30.8 (was 29.8)
    ('part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.8.html',
     block([
        ('<strong>Q1:</strong> Why is a guardrail that blocks 99.9% of adversarial inputs not "secure," and what must change about how you measure red-team success?',
         'A 99.9% block rate still allows 1 in 1,000 attempts through. A motivated attacker can automate thousands of requests per hour, making this a viable exploit. Red-team success must be measured statistically (attack success rate across N trials at a specified confidence level) rather than as binary pass/fail. LLM security is more like auditing a casino (the house must win on average) than testing a door lock (either it opens or it does not).'),
        ('<strong>Q2:</strong> A red team finds a persona attack that succeeds 3% of the time. Your manager says "3% is negligible." How do you reframe the risk?',
         'At 1,000 requests per day, 3% means 30 successful policy violations daily &mdash; not negligible. Reframe: "30 incidents per day is not acceptable regardless of percentage." Remediation: add persona-refusal training to the safety fine-tune, add an output classifier that flags known jailbreak response patterns, add the attack to the automated regression suite so every future model update is tested against it.'),
        ('<strong>Q3:</strong> How does indirect prompt injection in a RAG system differ from a direct user jailbreak, and why does it require a different defense strategy?',
         'Direct injection comes from user input and can be filtered at ingestion. Indirect injection is embedded in retrieved documents (web pages, emails, database records) that the system treats as trusted context; the user may be entirely innocent. Defense must focus on the retrieval pipeline: sanitize retrieved content before insertion, treat retrieved text with lower trust than system instructions, deploy a secondary LLM-based injection detector to scan retrieved chunks before they enter the main context.'),
     ])),
]


def main() -> int:
    n_added = 0
    n_skip = 0
    n_missing = 0
    for rel_path, body in INSERTIONS:
        p = ROOT / rel_path
        if not p.exists():
            print(f'  MISSING: {rel_path}')
            n_missing += 1
            continue
        text = p.read_text(encoding='utf-8', errors='replace')
        if SENTINEL in text:
            n_skip += 1
            continue
        # Insert right before the chapter-nav at the end (so it appears
        # before the prev/next links).
        nav_match = re.search(r'<nav\s+class="chapter-nav"', text, re.IGNORECASE)
        if not nav_match:
            print(f'  NO chapter-nav: {rel_path}')
            continue
        ins = nav_match.start()
        new = text[:ins] + body + text[ins:]
        p.write_text(new, encoding='utf-8')
        n_added += 1
        print(f'  added: {rel_path}')
    print(f'\nAdded {n_added}; skipped {n_skip}; missing {n_missing}.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
