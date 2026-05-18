"""Add <figcaption> elements to LLMBook figures that lack them.

Inserts a single <figcaption><strong>Figure X.Y.Z</strong>: ...</figcaption>
just before </figure> for the 14 captionless content figures identified
by the figure audit. Decorative chapter-opener, part-opener, and social-icon
figures are intentionally skipped.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

EDITS = [
    {
        "file": "part-11-llm-ethics-trust-governance/module-56-responsible-ai-tools/section-56.1.html",
        "figure_num": "56.1.3",
        "unique_anchor": 'aria-label="Responsible AI platform map"',
        "caption": (
            "A 2026 view of the Responsible AI platform landscape, grouping "
            "vendors into governance suites, hyperscaler bundles, "
            "observability tools, fairness toolkits, and policy-aligned "
            "frameworks."
        ),
    },
    {
        "file": "part-12-llm-systems-at-scale/module-61-scale-tools/section-61.1.html",
        "figure_num": "61.1.3",
        "unique_anchor": 'aria-label="LLM scale platform stack map"',
        "caption": (
            "The 2026 LLM training platform stack, from hyperscaler clouds "
            "at the bottom up through schedulers, experiment trackers, and "
            "observability tools that together turn raw GPUs into shipping "
            "training runs."
        ),
    },
    {
        "file": "part-12-llm-systems-at-scale/module-61-scale-tools/section-61.2.html",
        "figure_num": "61.2.1",
        "unique_anchor": 'aria-label="LLM training library stack"',
        "caption": (
            "The 2026 LLM training library stack: core frameworks (PyTorch, "
            "JAX), distributed engines (FSDP, DeepSpeed, Megatron), and "
            "orchestration layers that push MFU toward its theoretical "
            "ceiling."
        ),
    },
    {
        "file": "part-12-llm-systems-at-scale/module-61-scale-tools/section-61.3.html",
        "figure_num": "61.3.1",
        "unique_anchor": 'aria-label="LLM data and benchmark stack"',
        "caption": (
            "The 2026 LLM data and benchmark stack, spanning crawl-scale "
            "corpora, streaming pretraining loaders, evaluation suites, and "
            "benchmark hubs that anchor reproducible scaling work."
        ),
    },
    {
        "file": "part-12-llm-systems-at-scale/module-61-scale-tools/section-61.4.html",
        "figure_num": "61.4.1",
        "unique_anchor": 'aria-label="2026 model landscape"',
        "caption": (
            "The 2026 LLM model landscape grouped by serving footprint, "
            "from edge-class small models through mid-sized open weights up "
            "to flagship closed and frontier models that need multi-node "
            "hosts."
        ),
    },
    {
        "file": "part-12-llm-systems-at-scale/module-61-scale-tools/section-61.5.html",
        "figure_num": "61.5.1",
        "unique_anchor": 'aria-label="LLM scale reading and community map"',
        "caption": (
            "The 2026 reading and community landscape for LLM systems at "
            "scale: papers, model hubs, leaderboards, blogs, conferences, "
            "and chat communities that keep practitioners current."
        ),
    },
    {
        "file": "part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.1.html",
        "figure_num": "18.1.2",
        "unique_anchor": 'src="images/huyenchip-rlhf-pipeline.png"',
        "caption": (
            "The full ChatGPT-style training pipeline in three phases: "
            "pretraining on web-scale text, supervised fine-tuning on "
            "demonstration data, and RLHF optimization against a learned "
            "reward model."
        ),
    },
    {
        "file": "part-5-multimodal-llms/module-24-vla-models/section-24.6.html",
        "figure_num": "24.6.3",
        "unique_anchor": 'src="images/comic-nested-safety-vests.jpg"',
        "caption": (
            "A VLA-era safety story: no single layer is enough, so "
            "production robots wear nested vests of collision avoidance, "
            "hardware force limits, and anomaly detection on the action "
            "stream."
        ),
    },
    {
        "file": "part-6-agentic-ai/module-26-ai-agents/section-26.5.html",
        "figure_num": "26.5.8",
        "unique_anchor": 'aria-label="Production agent pipeline:',
        "caption": (
            "Reference architecture for a production agent: a request flows "
            "through the Permissions Gate, Cost Controller, Memory Manager, "
            "Planner, Tool Router, Execution Sandbox, Evaluator, and "
            "Recovery Handler."
        ),
    },
    {
        "file": "part-6-agentic-ai/module-29-specialized-agents/section-29.1.html",
        "figure_num": "29.1.3",
        "unique_anchor": 'src="images/comic-self-debug-strip.jpg"',
        "caption": (
            "The self-debugging loop that distinguishes a code agent from a "
            "completion tool: write code, run the tests, read the failures, "
            "edit, and repeat until the suite turns green."
        ),
    },
    {
        "file": "part-8-conversational-ai-with-llms/module-41-conv-ai-tools/section-41.1.html",
        "figure_num": "41.1.1",
        "unique_anchor": 'aria-label="Conversational AI platform map"',
        "caption": (
            "The 2026 conversational AI platform landscape: hosted authoring "
            "platforms, code-first orchestration frameworks, and "
            "bring-your-own-model API layers that all converge on "
            "chat-shaped products."
        ),
    },
    {
        "file": "part-8-conversational-ai-with-llms/module-41-conv-ai-tools/section-41.2.html",
        "figure_num": "41.2.4",
        "unique_anchor": 'aria-label="Chat orchestration framework selection"',
        "caption": (
            "A decision aid for picking a chat orchestration framework, "
            "mapping team profile, hosting preference, and feature gravity "
            "(graphs, tools, observability) onto the leading 2026 options."
        ),
    },
    {
        "file": "part-8-conversational-ai-with-llms/module-41-conv-ai-tools/section-41.3.html",
        "figure_num": "41.3.3",
        "unique_anchor": 'aria-label="Conversational AI evaluation pyramid"',
        "caption": (
            "The 2026 conversational AI evaluation pyramid: cheap automatic "
            "metrics at the base, LLM-as-judge in the middle, and expensive "
            "human-in-the-loop plus production telemetry at the top."
        ),
    },
    {
        "file": "part-8-conversational-ai-with-llms/module-41-conv-ai-tools/section-41.4.html",
        "figure_num": "41.4.3",
        "unique_anchor": 'aria-label="Chat model selection axes"',
        "caption": (
            "Four axes for picking a chat model in 2026: capability tier, "
            "hosting and privacy posture, latency and cost envelope, and the "
            "persona or domain fit the product requires."
        ),
    },
]


def main(dry_run: bool = False) -> None:
    figure_re = re.compile(r"<figure\b[^>]*>(.*?)</figure>", re.DOTALL | re.IGNORECASE)
    changes = []
    for e in EDITS:
        f = ROOT / e["file"]
        text = f.read_text(encoding="utf-8")

        # Sanity-check uniqueness of the anchor
        occ = text.count(e["unique_anchor"])
        if occ != 1:
            raise SystemExit(
                f"Anchor not unique in {e['file']}: '{e['unique_anchor']}' "
                f"occurs {occ}x"
            )

        # Find the single figure whose body contains the anchor and lacks a figcaption
        target = None
        for m in figure_re.finditer(text):
            body = m.group(1)
            if e["unique_anchor"] not in body:
                continue
            if "<figcaption" in body.lower():
                raise SystemExit(
                    f"Figure already has caption in {e['file']}"
                )
            target = m
            break
        if target is None:
            raise SystemExit(
                f"No matching captionless figure in {e['file']} for anchor "
                f"'{e['unique_anchor']}'"
            )

        # Build the figcaption (no em dashes, canonical format)
        cap = e["caption"].strip()
        if "—" in cap or "--" in cap:
            raise SystemExit(f"Caption contains em dash for {e['file']}")
        figcap = (
            f'<figcaption><strong>Figure {e["figure_num"]}</strong>: '
            f"{cap}</figcaption>\n"
        )

        # Find the </figure> for this match and insert figcap immediately before it
        end_of_figure = target.end()
        # target.end() lies right after </figure>. Compute index of "</figure>"
        close_idx = text.rfind("</figure>", target.start(), end_of_figure)
        if close_idx < 0:
            raise SystemExit(f"Cannot locate </figure> in {e['file']}")

        new_text = text[:close_idx] + figcap + text[close_idx:]
        if not dry_run:
            f.write_text(new_text, encoding="utf-8")
        changes.append(
            (e["file"], e["figure_num"], len(cap), close_idx)
        )

    print(f"Processed {len(changes)} edits (dry_run={dry_run})")
    for f, num, ln, idx in changes:
        print(f"  {f} -> Figure {num} ({ln} chars caption)")


if __name__ == "__main__":
    import sys
    main(dry_run="--dry-run" in sys.argv)
