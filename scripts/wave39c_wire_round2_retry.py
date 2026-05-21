"""Wave 39c retry: wire 8 round-2 comic callouts with corrected anchors."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from wave37_wire_comics import make_callout

ROOT = Path(__file__).resolve().parents[1]

INSERTIONS = [
    {
        'file': 'part-9-llm-evaluation-observability/module-46-llm-as-judge-automated-evaluation/section-46.1.html',
        'src': 'images/comic-gpt4-mirror.png',
        'after_text': '<h2 id="46-1-1-judge-bias-taxonomy">46.1.1 Judge Bias Taxonomy</h2>',
        'callout': make_callout('fun-note', 'Fun Fact: The judge grades the mirror',
            'A cartoon GPT-4 character holding a hand-mirror up to its own face, while writing 5/5 Excellent on a clipboard.',
            'images/comic-gpt4-mirror.png',
            '<strong>Figure 46.1.2</strong>: Self-preference bias. The same model evaluating its own output systematically scores it higher than blind raters do.'),
    },
    {
        'file': 'part-9-llm-evaluation-observability/module-46-llm-as-judge-automated-evaluation/section-46.1.html',
        'src': 'images/comic-judge-five-biases.png',
        'after_text': '<h2 id="46-1-1-judge-bias-taxonomy">46.1.1 Judge Bias Taxonomy</h2>',
        'callout': make_callout('fun-note', 'Fun Fact: All five weights on the same side',
            'A cartoon judge in a wig holding a balance scale. Five weights labelled Position, Length, Self-preference, Anchoring, Style are stacked on the same side.',
            'images/comic-judge-five-biases.png',
            '<strong>Figure 46.1.3</strong>: Judge biases compound rather than cancel. A single LLM judge needs position-swap, length-control, blind-cohort, anchoring-mitigation, and style-normalization to keep its scale level.'),
    },
    {
        'file': 'part-12-llm-systems-at-scale/module-59-distributed-training-systems/section-59.5.html',
        'src': 'images/comic-3am-checkpoint.png',
        'after_text': '<h2 id="59-5-2-checkpointing-strategies">59.5.2 Checkpointing Strategies</h2>',
        'callout': make_callout('fun-note', 'Fun Fact: 3 AM saves the run',
            'A training-cluster scene at 3am. One GPU server smokes. A robot labelled auto-checkpoint carries the model state in a treasure chest labelled S3 to safety. The on-call engineer watches in pajamas with coffee.',
            'images/comic-3am-checkpoint.png',
            '<strong>Figure 59.5.3</strong>: The most boring graph in a training postmortem is the checkpoint-cadence chart. Boring is the goal.'),
    },
    {
        'file': 'part-12-llm-systems-at-scale/module-61-scale-tools/section-61.1.html',
        'src': 'images/comic-ethernet-vs-infiniband.png',
        'after_text': '<h2 id="61-1-2-specialized-gpu-clouds">61.1.2 Specialized GPU clouds</h2>',
        'callout': make_callout('fun-note', 'Fun Fact: The silent multiplier',
            'Two cartoon GPU clusters side-by-side. Left: Ethernet, thin droopy wires, sad GPUs at 30% MFU. Right: InfiniBand, thick glowing cables, happy GPUs at 60% MFU.',
            'images/comic-ethernet-vs-infiniband.png',
            '<strong>Figure 61.1.2</strong>: The interconnect, not the GPU, often sets the throughput ceiling on 1024+ GPU jobs.'),
    },
    {
        'file': 'part-8-conversational-ai-with-llms/module-41-conv-ai-tools/section-41.3.html',
        'src': 'images/comic-arena-wrestling.png',
        'after_text': '<h2 id="41-3-3-preference-and-judgment-benchmarks">41.3.3 Preference and judgment benchmarks for chat models</h2>',
        'callout': make_callout('fun-note', 'Fun Fact: Two robots, blindfolded humans, one Elo number',
            'Two anonymized cartoon chatbots arm-wrestling on a stage with masks labelled Model A and Model B. A crowd of blindfolded humans raises A and B paddles. Scoreboard reads ELO 1230 vs 1228.',
            'images/comic-arena-wrestling.png',
            '<strong>Figure 41.3.2</strong>: LMSYS Arena anonymizes contestants and trusts crowd-pairwise voting. The Bradley-Terry model converts those votes into an Elo number.'),
    },
    {
        'file': 'part-8-conversational-ai-with-llms/module-41-conv-ai-tools/section-41.4.html',
        'src': 'images/comic-cascaded-vs-realtime.png',
        'after_text': '<h2 id="41-4-2-voice-aware-models">41.4.2 Voice-aware models for realtime conversation</h2>',
        'callout': make_callout('fun-note', 'Fun Fact: The flash cards vs the coffee cup',
            'Telephone-call split panel. Left robot labelled cascaded pipeline holds flash cards labelled STT, LLM, TTS, looks stressed. Right robot labelled GPT-4o Realtime sips coffee, mid-sentence.',
            'images/comic-cascaded-vs-realtime.png',
            '<strong>Figure 41.4.2</strong>: Cascaded voice pipelines pay the latency tax of intermediate text. Realtime speech-to-speech models avoid the cascade.'),
    },
    {
        'file': 'part-5-multimodal-llms/module-24-vla-models/section-24.13.html',
        'src': 'images/comic-domain-randomization-globe.png',
        'after_text': '<h2 id="24-13-2-domain-randomization">24.13.2 Domain Randomization, the Workhorse</h2>',
        'callout': make_callout('fun-note', 'Fun Fact: Domain randomization in one snow globe',
            'A snow globe containing a robot arm on a table. A giant hand shakes it. Labels float around inside: lighting, friction, mass, camera_jitter. A researcher outside holds a clipboard labelled Domain Randomization.',
            'images/comic-domain-randomization-globe.png',
            '<strong>Figure 24.13.2</strong>: Domain randomization shakes the simulation until the model gives up on memorizing any one configuration and learns the underlying skill.'),
    },
    {
        'file': 'part-6-agentic-ai/module-29-specialized-agents/section-29.1.html',
        'src': 'images/comic-self-debug-strip.png',
        'after_text': '<h2 id="29-1-2-three-named-architectural-patterns">29.1.2 Three Named Architectural Patterns</h2>',
        'callout': make_callout('fun-note', 'Fun Fact: The self-debug loop, in four panels',
            'Four-panel strip. Panel 1: robot types code. Panel 2: tests window shows 3 RED 2 GREEN, robot frowns. Panel 3: robot scratches head while editing. Panel 4: tests now 5 GREEN, robot lifts arms.',
            'images/comic-self-debug-strip.png',
            '<strong>Figure 29.1.2</strong>: The self-debugging loop. Empirically k=3-5 iterations is where SWE-bench accuracy saturates.'),
    },
]


def main():
    n = 0
    for ins in INSERTIONS:
        path = ROOT / ins['file']
        text = path.read_text(encoding='utf-8')
        if ins['src'] in text:
            print(f'  SKIP (already): {ins["src"]}')
            continue
        idx = text.find(ins['after_text'])
        if idx == -1:
            print(f'  NO ANCHOR: {ins["after_text"][:70]!r}')
            continue
        line_end = text.find('\n', idx + len(ins['after_text']))
        if line_end == -1:
            line_end = idx + len(ins['after_text'])
        new = text[:line_end + 1] + ins['callout'] + text[line_end + 1:]
        path.write_text(new, encoding='utf-8')
        n += 1
        print(f'  WIRED {ins["src"]}')
    print(f'\nWired {n}')


if __name__ == '__main__':
    main()
