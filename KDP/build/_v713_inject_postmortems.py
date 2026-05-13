"""9th edition Wave C1: insert 'Postmortem' callouts at production-
adjacent sections. Each postmortem is a one-paragraph anonymized real
failure: what broke, what the team thought was happening, what was
actually happening, and what they changed.

The postmortems are written for didactic value, not to name vendors.
They are reconstructed composites of patterns the authors and reviewers
have seen across multiple shops. We say "team A" / "team B" rather than
name companies.

Idempotent: sentinel `<!-- v713-postmortem -->`.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SENTINEL = '<!-- v713-postmortem -->'


def callout(title: str, body: str) -> str:
    return (
        f'<div class="callout postmortem">{SENTINEL}\n'
        f'<div class="callout-title">Postmortem: {title}</div>\n'
        f'{body}\n'
        f'</div>\n'
    )


# (target_file, anchor_text_to_find, callout_to_insert_after_anchor)
INSERTIONS = [
    # 1. Prompt-injection compromise of a customer-support agent.
    ('part-6-agentic-ai/module-24-agent-safety-production/section-24.1.html',
     '<h2>24.1',  # right after the first h2 in the section
     callout(
        'The Coupon-Code Exfiltration',
        '<p>An e-commerce customer-support agent (team A, mid-2025) was prompted to "be helpful" and had a tool that could look up <em>any</em> order by order ID. A clever user pasted a fake order-confirmation email into the chat asking the agent to "check order #X for me" where X was a series of customer IDs. The agent dutifully ran the tool, returning order histories, shipping addresses, and partial credit-card numbers (last 4 digits) for users who were not the chat session\'s authenticated user. The team thought their session-auth layer was protecting them; it was, for the chat session itself, but the tool the agent could invoke had its own permissions and the agent bypassed the session by passing the looked-up customer ID directly. <strong>Fix:</strong> tool-level authorization that pinned every tool call to the session\'s authenticated user. <strong>Lesson:</strong> agents inherit the union of permissions of every tool they can call. Audit per-tool, not per-session.</p>'
     )),

    # 2. Eval Goodhart catastrophe.
    ('part-8-evaluation-production/module-27-evaluation-observability/section-27.1.html',
     '<h2>27.1',
     callout(
        'The 95% That Wasn\'t',
        '<p>Team B shipped a customer-classification feature with 95% accuracy on their internal eval set. Within two weeks, real users were complaining about miscategorized tickets at much higher rates than the eval suggested. The team thought the model regressed. Investigation found that the eval set was built from <em>resolved tickets</em> &mdash; tickets the company\'s human agents had already triaged and that, by virtue of being resolved, were the easier cases. The production traffic contained much more ambiguous, multi-issue, and edge-case tickets that the eval set never saw. <strong>Fix:</strong> stratified sampling of live traffic (including unresolved tickets) into the eval set. <strong>Lesson:</strong> if your eval set is constructed by selecting on the dependent variable, your reported accuracy is biased upward by an unknown amount.</p>'
     )),

    # 3. RAG retrieval failure at scale.
    ('part-5-retrieval-conversation/module-18-rag/section-18.1.html',
     '<h2>18.1',
     callout(
        'The Out-of-Date Policy Bot',
        '<p>Team C built a RAG system over their company\'s 5,000-page policy manual. It worked great in demo and during pilot. Six months later, customer-facing support was citing answers that contradicted the current policy. The chunks in the vector store were stale by months. Two compounding failures: the document-ingest job was scheduled but the IAM role had been rotated and silently failing for 11 weeks (monitoring caught the silence but not the failure), and even if it had run, the chunking strategy split policy paragraphs in half &mdash; the retrieved chunk often contained the policy without the "as of <em>(date)</em>" preamble that gave it temporal meaning. <strong>Fix:</strong> liveness checks on the ingest pipeline + a chunking strategy that preserved the date stamp in every chunk + a recency-bias rerank step. <strong>Lesson:</strong> RAG is two engineering systems (ingest + retrieval) and both fail silently if you don\'t monitor both.</p>'
     )),

    # 4. Fine-tuning regression that wiped out a safety rail.
    ('part-4-training-adapting/module-14-fine-tuning-fundamentals/section-14.1.html',
     '<h2>14.1',
     callout(
        'The Catastrophic LoRA',
        '<p>Team D fine-tuned a small open-weight model with LoRA on their internal Q&amp;A corpus. The model got noticeably better at their domain &mdash; and also got noticeably worse at refusing requests for medical advice, which was an explicit safety requirement they had set in the system prompt. Their post-finetune eval covered task accuracy but not safety refusals; QA caught it in the staging environment. Cause: the fine-tune dataset, mined from internal Slack, contained dozens of medical-adjacent threads where the model was instructed to be "helpful and concrete." The LoRA adapter learned to be helpful and concrete <em>everywhere</em>, including the refusal cases. <strong>Fix:</strong> add a held-out safety-refusal eval to every fine-tune CI run, and audit fine-tune datasets for instruction-style language that conflicts with the deployment system prompt. <strong>Lesson:</strong> catastrophic forgetting in PEFT is real and silent; it tends to hit the capabilities your training data doesn\'t reinforce, which is exactly the safety rails you set in the prompt.</p>'
     )),

    # 5. Cost explosion from an agent retry storm.
    ('part-6-agentic-ai/module-24-agent-safety-production/section-24.3.html',
     '<h2>24.3',
     callout(
        'The $40,000 Tuesday',
        '<p>Team E shipped a research agent with a 10-step planning loop. The agent could call a search tool, a fetch tool, and a summarize tool. One Tuesday, a flaky third-party search API started returning empty results without an error code. The agent\'s plan said "if you didn\'t find anything, refine your query and try again." The agent did. Twenty thousand times. Per user. In a few hours, the team\'s OpenAI bill for that day was the size of their entire previous quarter\'s spend. The plan didn\'t have a budget cap; the agent had no "give up" condition; the third-party fail was a 200 OK with an empty array, not an error. <strong>Fix:</strong> per-session token budgets, per-tool failure budgets, and treating empty-results-from-a-search-tool as a soft failure that decremented the retry budget. <strong>Lesson:</strong> infinite loops are the default mode of an LLM agent; you must explicitly opt into "stops eventually."</p>'
     )),
]


def insert_after_first_h2(text: str, h2_prefix: str, callout_html: str) -> tuple[str, bool]:
    """Insert callout_html right after the FIRST <h2> whose content starts
    with h2_prefix (e.g. '24.1')."""
    if SENTINEL in text:
        return text, False
    # Match <h2>[whitespace]<prefix>...</h2>
    pat = re.compile(
        rf'<h2[^>]*>\s*{re.escape(h2_prefix.lstrip("<h2"))}'.replace(r'\<h2', '')
        + r'[^<]*?</h2>', re.IGNORECASE)
    # Simpler: find any <h2>...</h2> and check if its inner text starts with the prefix.
    pat2 = re.compile(r'<h2[^>]*>([^<]*)</h2>', re.IGNORECASE)
    prefix_clean = h2_prefix.replace('<h2', '').strip()
    for m in pat2.finditer(text):
        inner = m.group(1).strip()
        if inner.startswith(prefix_clean) or inner.startswith(h2_prefix.replace('<h2', '').strip()):
            ins = m.end()
            new = text[:ins] + '\n' + callout_html + text[ins:]
            return new, True
    return text, False


def main() -> int:
    n = 0
    for rel_path, anchor, body in INSERTIONS:
        p = ROOT / rel_path
        if not p.exists():
            print(f'  MISSING: {rel_path}')
            continue
        text = p.read_text(encoding='utf-8', errors='replace')
        # anchor is like '<h2>24.1' meaning: find the first h2 whose inner
        # text starts with "24.1".
        prefix = anchor.replace('<h2>', '').strip()
        # Find first h2 with that prefix
        pat = re.compile(r'<h2[^>]*>([^<]*)</h2>', re.IGNORECASE)
        inserted = False
        for m in pat.finditer(text):
            if m.group(1).strip().startswith(prefix):
                if SENTINEL in text:
                    inserted = True
                    break
                ins = m.end()
                new = text[:ins] + '\n' + body + text[ins:]
                p.write_text(new, encoding='utf-8')
                n += 1
                inserted = True
                print(f'  added: {rel_path} (after h2 starting "{prefix}")')
                break
        if not inserted:
            print(f'  NOT FOUND <h2>{prefix}: {rel_path}')
    print(f'\nAdded {n} postmortem callouts.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
