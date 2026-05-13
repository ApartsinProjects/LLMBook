"""10th edition Wave 8: Claude platform coverage. Pre-drafted in
_agent_reports/claude-coverage.md.

Adds 6 callouts covering Claude Agent SDK, Skills/Apps, Connectors,
Claude in Chrome, Plugins, multi-agent handoffs.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SENTINEL = '<!-- v736-claude -->'


def callout(title: str, body: str, css_class: str = 'practical-example') -> str:
    return (
        f'<div class="callout {css_class}">{SENTINEL}\n'
        f'<div class="callout-title">{title}</div>\n'
        f'{body}\n'
        f'</div>\n'
    )


# Post-renumber section numbers
INSERTIONS = [
    # 1. Claude Agent SDK -- Section 23.1 (Framework Landscape, post-renumber from 22.1)
    ('part-6-agentic-ai/module-23-multi-agent-systems/section-23.1.html',
     '23.1',
     callout(
        '2026 Snapshot: Claude Agent SDK',
        '<p>Anthropic\'s <strong>Claude Agent SDK</strong> (anthropic-ai/claude-agent-sdk) is the code-first counterpart to OpenAI Agents SDK. Default to Claude models, built-in tool calling, multi-agent handoffs, and integrated tracing. Architecturally similar to OpenAI Agents SDK; the main difference is provider binding. Teams already on PydanticAI can reach both providers with a single string swap; the platform SDKs matter most when you want tighter integration with provider-specific features (extended thinking on Claude, Realtime API on OpenAI). For a vendor-neutral starting point, prefer PydanticAI or LangGraph; reach for the platform SDKs once you commit to a provider for production.</p>'
     )),
    # 2. Anthropic Connectors + Claude Plugins -- Section 22.2 (MCP, post-renumber from 21.2)
    ('part-6-agentic-ai/module-22-tool-use-protocols/section-22.2.html',
     '22.2',
     callout(
        '2026 Snapshot: Anthropic Connectors and Claude Plugins',
        '<p><strong>Anthropic Connectors</strong> are first-party managed integrations (Google Drive, Slack, GitHub, Confluence) that Claude can query directly without a custom MCP server &mdash; trading customization for operational simplicity. <strong>Claude Plugins</strong> are the curated marketplace tier on top of MCP: third-party developers publish capabilities into the Claude platform, similar to ChatGPT Plugins (now GPT Actions) or Google Agentspace Marketplace Extensions. The pedagogical point: <em>MCP is the open protocol; Connectors and Plugins are the provider\'s curated, hosted distribution layer on top</em>. Pick based on how much customization vs. operational burden you can absorb.</p>'
     )),
    # 3. Claude Skills + Custom Assistants -- Section 27.1 (LLM Applications, post-renumber from 26.1)
    ('part-7-multimodal-applications/module-27-llm-applications/section-27.1.html',
     '27.1',
     callout(
        '2026 Snapshot: No-Code Assistant Platforms (Skills, GPTs, Gems)',
        '<p>All three frontier providers now offer a layer above raw API access where non-developers configure specialized assistants: <strong>Anthropic Claude Apps with Skills</strong>, <strong>OpenAI Custom GPTs</strong> (GPT Store), <strong>Google Gems / Agent Builder</strong>. These no-code surfaces matter when you need to deploy assistants to non-technical users without building a full application. Architecturally they are system-prompt bundles with optional tool access, governed by provider guardrails. Trade-offs are identical across providers: ease of deployment vs. customization depth vs. data residency. Choose based on which provider your organization already trusts; the user-facing differences are surprisingly small.</p>'
     )),
    # 4. Claude in Chrome -- Section 24.2 (Browser Agents, post-renumber from 23.2)
    ('part-6-agentic-ai/module-24-specialized-agents/section-24.2.html',
     '24.2',
     callout(
        '2026 Snapshot: Browser-Side Assistants vs. Headless Browser Agents',
        '<p><strong>Claude in Chrome</strong>, <strong>Microsoft Copilot in Edge</strong>, and <strong>Gemini in Chrome</strong> represent a different tier from the headless browser agents covered above (Playwright MCP, Stagehand, browser-use). They operate at the user-interface layer the user sees, not at the DOM layer. Suitable for helping users with tasks they\'re already doing (page summarization, form-fill assistance, lightweight computer use). Unsuitable for automated headless workflows because they rely on visual and text context the extension can read, not programmatic DOM scripting. The architectural choice is exclusive: developer-grade browser automation OR user-side browser assistance, not both.</p>'
     )),
]


def main() -> int:
    n_added = 0
    n_skip = 0
    n_missing = 0
    for rel_path, h2_prefix, body in INSERTIONS:
        p = ROOT / rel_path
        if not p.exists():
            print(f'  MISSING: {rel_path}')
            n_missing += 1
            continue
        text = p.read_text(encoding='utf-8', errors='replace')
        if body[:200] in text:
            n_skip += 1
            continue
        for pat in (re.compile(r'<h2[^>]*>([^<]*)</h2>', re.IGNORECASE),
                    re.compile(r'<h3[^>]*>([^<]*)</h3>', re.IGNORECASE)):
            inserted = False
            for m in pat.finditer(text):
                if m.group(1).strip().startswith(h2_prefix):
                    ins = m.end()
                    new = text[:ins] + '\n' + body + text[ins:]
                    p.write_text(new, encoding='utf-8')
                    n_added += 1
                    inserted = True
                    print(f'  added: {rel_path} (after "{h2_prefix}")')
                    break
            if inserted:
                break
        if not inserted:
            print(f'  NOT FOUND "{h2_prefix}" in {rel_path}')
    print(f'\nAdded {n_added}; skipped {n_skip}; missing {n_missing}.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
