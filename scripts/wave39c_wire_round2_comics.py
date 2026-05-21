"""Wave 39c: Wire 9 round-2 comic images into HTML sections.

Defers ch56-2-three-fairness-scales because section-56.2 is being edited by
the running library-shortcut agent.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from wave37_wire_comics import make_callout

ROOT = Path(__file__).resolve().parents[1]
INSERT_AFTER_MAIN = re.compile(r'(<main\s+class="content"[^>]*>\s*)', re.IGNORECASE)


INSERTIONS = [
    # Ch 46.1 GPT-4 mirror — top of section after first h2
    {
        'file': 'part-9-llm-evaluation-observability/module-46-llm-as-judge-automated-evaluation/section-46.1.html',
        'src': 'images/comic-gpt4-mirror.png',
        'after_text': '<h2 id="46-1-1-why-llm-as-judge-matters">46.1.1 Why LLM-as-Judge Matters</h2>',
        'callout': make_callout(
            'fun-note',
            'Fun Fact: The judge grades the mirror',
            'A cartoon GPT-4 character holding a hand-mirror up to its own face, while writing 5/5 Excellent on a clipboard. A caption banner reads Self-Preference Bias In Action.',
            'images/comic-gpt4-mirror.png',
            '<strong>Figure 46.1.2</strong>: Self-preference bias is the most reliable failure mode of LLM-as-judge. The same model evaluating its own output systematically scores it higher than blind raters do.',
        ),
    },
    # Ch 46.1 five biases scale
    {
        'file': 'part-9-llm-evaluation-observability/module-46-llm-as-judge-automated-evaluation/section-46.1.html',
        'src': 'images/comic-judge-five-biases.png',
        'after_text': '<h2 id="46-1-2-the-five-canonical-judge-biases">46.1.2 The Five Canonical Judge Biases</h2>',
        'callout': make_callout(
            'fun-note',
            'Fun Fact: All five weights on the same side',
            'A cartoon judge in a wig holding a balance scale. Five small weights labelled Position, Length, Self-preference, Anchoring, Style are all stacked on the same side. The judge looks puzzled.',
            'images/comic-judge-five-biases.png',
            '<strong>Figure 46.1.3</strong>: Judge biases compound rather than cancel. A single LLM judge needs each of position-swap, length-control, blind-cohort, anchoring-mitigation, and style-normalization to keep its scale level.',
        ),
    },
    # Ch 56.1 Venn buyers
    {
        'file': 'part-11-llm-ethics-trust-governance/module-56-responsible-ai-tools/section-56.1.html',
        'src': 'images/comic-venn-buyers.png',
        'after_text': '<h2 id="56-1-1-enterprise-governance-platforms">56.1.1 Enterprise governance platforms</h2>',
        'callout': make_callout(
            'fun-note',
            'Fun Fact: Three buyers, three platforms, zero overlap',
            'A friendly Venn diagram cartoon. Three large overlapping circles labelled General Counsel, CDO, CISO. Each circle points to a different platform icon. The three-way intersection is empty and labelled One Platform To Rule Them All (theoretical).',
            'images/comic-venn-buyers.png',
            '<strong>Figure 56.1.2</strong>: Most enterprises end up with two governance platforms, not one, because Legal, Data, and Security each frame "Responsible AI" differently and each pick what their compliance language demands.',
        ),
    },
    # Ch 59.5 3am checkpoint
    {
        'file': 'part-12-llm-systems-at-scale/module-59-distributed-training-systems/section-59.5.html',
        'src': 'images/comic-3am-checkpoint.png',
        'after_text': '<h2 id="59-5-2-checkpointing-and-recovery">59.5.2 Checkpointing and Recovery</h2>',
        'callout': make_callout(
            'fun-note',
            'Fun Fact: 3 AM saves the run',
            'A cartoon training-cluster scene at 3am. One of many GPU servers is comically smoking. A small friendly robot labelled auto-checkpoint calmly carries the model state in a tiny treasure chest labelled S3 to safety. The on-call engineer stands nearby in pajamas with coffee.',
            'images/comic-3am-checkpoint.png',
            '<strong>Figure 59.5.3</strong>: The most boring graph in a training postmortem is the checkpoint-cadence chart. Boring is the goal: every minute of $T^* = \\sqrt{2 C \\tau}$ that the system skipped, the human had to make up at 3 AM.',
        ),
    },
    # Ch 61.1 ethernet vs InfiniBand
    {
        'file': 'part-12-llm-systems-at-scale/module-61-scale-tools/section-61.1.html',
        'src': 'images/comic-ethernet-vs-infiniband.png',
        'after_text': '<h2 id="61-1-3-interconnects">61.1.3 Interconnects</h2>',
        'callout': make_callout(
            'fun-note',
            'Fun Fact: The silent multiplier',
            'Two cartoon GPU clusters side-by-side. Left: labelled Ethernet, with thin droopy wires and sad GPUs achieving 30% MFU. Right: labelled InfiniBand, with thick glowing cables and happy GPUs at 60% MFU. Caption banner: Interconnect Is The Silent Multiplier.',
            'images/comic-ethernet-vs-infiniband.png',
            '<strong>Figure 61.1.2</strong>: The interconnect, not the GPU, often sets the throughput ceiling on 1024+ GPU jobs. The MFU gap between Ethernet and InfiniBand is real and reverses the headline cost comparison.',
        ),
    },
    # Ch 41.3 arena
    {
        'file': 'part-8-conversational-ai-with-llms/module-41-conv-ai-tools/section-41.3.html',
        'src': 'images/comic-arena-wrestling.png',
        'after_text': '<h2 id="41-3-2-the-arena-era-lmsys-and-anonymized-pairwise-voting">41.3.2 The Arena era: LMSYS and anonymized pairwise voting</h2>',
        'callout': make_callout(
            'fun-note',
            'Fun Fact: Two robots, blindfolded humans, one Elo number',
            'Two anonymized cartoon chatbot characters arm-wrestling on a small stage with masks labelled Model A and Model B. A crowd of cartoon humans below wearing blindfolds raises A and B paddles. A scoreboard reads ELO 1230 vs 1228.',
            'images/comic-arena-wrestling.png',
            '<strong>Figure 41.3.2</strong>: LMSYS Arena anonymizes the contestants and trusts crowd-pairwise voting. The Bradley-Terry model converts those votes into an Elo number that, on its own, never tells you which model is actually wiser.',
        ),
    },
    # Ch 41.4 voice cascaded vs realtime
    {
        'file': 'part-8-conversational-ai-with-llms/module-41-conv-ai-tools/section-41.4.html',
        'src': 'images/comic-cascaded-vs-realtime.png',
        'after_text': '<h2 id="41-4-2-voice-aware-models">41.4.2 Voice-aware models</h2>',
        'callout': make_callout(
            'fun-note',
            'Fun Fact: The flash cards vs the coffee cup',
            'Telephone-call cartoon, split panel. Left robot labelled cascaded pipeline holds a stack of giant flash cards labelled STT, LLM, TTS and looks stressed. Right robot labelled GPT-4o Realtime sips coffee, relaxed, mid-sentence. A phone line connects them.',
            'images/comic-cascaded-vs-realtime.png',
            '<strong>Figure 41.4.2</strong>: Cascaded voice pipelines pay the latency tax of intermediate text. Realtime speech-to-speech models avoid the cascade by emitting audio tokens directly.',
        ),
    },
    # Ch 24.13 snow globe
    {
        'file': 'part-5-multimodal-llms/module-24-vla-models/section-24.13.html',
        'src': 'images/comic-domain-randomization-globe.png',
        'after_text': '<h2 id="24-13-2-domain-randomization">24.13.2 Domain Randomization</h2>',
        'callout': make_callout(
            'fun-note',
            'Fun Fact: Domain randomization in one snow globe',
            'A snow globe containing a tiny robot arm on a table. A giant hand shakes it. Tiny labels float around inside the globe: lighting, friction, mass, camera_jitter. Outside the globe, a researcher holds a clipboard labelled Domain Randomization.',
            'images/comic-domain-randomization-globe.png',
            '<strong>Figure 24.13.2</strong>: Domain randomization shakes the simulation until the model gives up on memorizing any one configuration and learns the underlying skill instead.',
        ),
    },
    # Ch 29.1 self-debug strip
    {
        'file': 'part-6-agentic-ai/module-29-specialized-agents/section-29.1.html',
        'src': 'images/comic-self-debug-strip.png',
        'after_text': '<h2 id="29-1-2-the-self-debugging-loop">29.1.2 The Self-Debugging Loop</h2>',
        'callout': make_callout(
            'fun-note',
            'Fun Fact: The self-debug loop, in four panels',
            'Four-panel cartoon strip. Panel 1: a robot types code on a laptop. Panel 2: a tests window shows 3 RED, 2 GREEN, robot frowns. Panel 3: robot scratches head while editing. Panel 4: tests now 5 GREEN, robot lifts arms in tiny triumph.',
            'images/comic-self-debug-strip.png',
            '<strong>Figure 29.1.2</strong>: The self-debugging loop. Empirically, k=3-5 iterations is where SWE-bench accuracy saturates: more attempts rarely fix new bugs and often confuse the agent into reverting earlier wins.',
        ),
    },
]


def main():
    n_inserted = 0
    for ins in INSERTIONS:
        path = ROOT / ins['file']
        if not path.exists():
            print(f'  SKIP (no file): {ins["file"]}')
            continue
        text = path.read_text(encoding='utf-8')
        if ins['src'] in text:
            print(f'  SKIP (already wired): {ins["src"]}')
            continue
        anchor = ins['after_text']
        idx = text.find(anchor)
        if idx == -1:
            print(f'  NO ANCHOR in {ins["file"]}: anchor={anchor[:60]!r}')
            continue
        line_end = text.find('\n', idx + len(anchor))
        if line_end == -1:
            line_end = idx + len(anchor)
        insertion_pt = line_end + 1
        new = text[:insertion_pt] + ins['callout'] + text[insertion_pt:]
        path.write_text(new, encoding='utf-8')
        n_inserted += 1
        print(f'  WIRED {ins["src"]}')
    print(f'\nWired {n_inserted} round-2 comic callouts')


if __name__ == '__main__':
    main()
