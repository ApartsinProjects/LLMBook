"""Wave 37: Wire 13 comic / mental-map images into book pages.

For each generated comic, locate a unique anchor in the target section and
insert a canonical callout (`fun-note` for comics, `key-insight` for mental
maps) containing a `<figure class="illustration">`. Idempotent: skips when
the figure src is already referenced in the file.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]


def make_callout(callout_type: str, title: str, alt: str, src: str, caption: str, body: str = "") -> str:
    parts = [
        f'<div class="callout {callout_type}">',
        f'<div class="callout-title">{title}</div>',
        f'<figure class="illustration">',
        f'<img alt="{alt}" src="{src}"/>',
        f'<figcaption>{caption}</figcaption>',
        f'</figure>',
    ]
    if body:
        parts.append(f'<p>{body}</p>')
    parts.append('</div>')
    return '\n'.join(parts) + '\n'


INSERTIONS = [
    # ch34-1 classical-vs-llm 4-panel strip: after Table 34.1.1 (comparison-table div close)
    {
        'file': 'part-7-retrieval-information-extraction-with-llms/module-34-structured-information-extraction-ner/section-34.1.html',
        'src': 'images/comic-classical-vs-llm-strip.png',
        'after_text': '<h3 id="34-1-1-1-classical-ie-vs-llm-based-ie">34.1.1.1 Classical IE vs. LLM-Based IE</h3>',
        'callout': make_callout(
            'fun-note',
            'Fun Fact: Classical NER vs LLM NER, in four panels',
            'A four-panel cartoon comparing classical NER (a clockwork spaCy robot) with an LLM wizard. The classical robot handles routine PERSON/ORG/DATE stamps efficiently but gives up on a novel medical_condition entity, which the LLM wizard then resolves at the cost of one tip-jar coin.',
            'images/comic-classical-vs-llm-strip.png',
            '<strong>Figure 34.1.2</strong>: The classical NER robot handles the easy cases at near-zero cost; the LLM wizard takes the weird ones for a per-document fee. The hybrid architecture in Section 34.3 lets both characters do what they are good at.',
        ),
    },
    # ch34-1 librarian-wizard: mental-map at top of section (key-insight)
    {
        'file': 'part-7-retrieval-information-extraction-with-llms/module-34-structured-information-extraction-ner/section-34.1.html',
        'src': 'images/comic-librarian-wizard.png',
        'after_text': '<h2 id="34-1-1-the-information-extraction-landscape">34.1.1 The Information Extraction Landscape</h2>',
        'callout': make_callout(
            'fun-note',
            'Fun Fact: The librarian and the wizard',
            'A cartoon librarian in glasses stamping books labeled PERSON, ORG, DATE with green checkmarks, while behind her a wizard in a blue hat conjures a glowing book labeled medical_condition out of thin air',
            'images/comic-librarian-wizard.png',
            '<strong>Figure 34.1.3</strong>: The librarian (classical NER) is fast and never makes things up. The wizard (LLM) is flexible and occasionally invents an author. Most production pipelines hire both.',
        ),
    },
    # ch34-3 hospital triage: after the production-pattern P10 callout
    {
        'file': 'part-7-retrieval-information-extraction-with-llms/module-34-structured-information-extraction-ner/section-34.3.html',
        'src': 'images/comic-hospital-triage.png',
        'after_text': '<div class="callout-title">Production Pattern P10: Two-Layer Hybrid IE Architecture</div>',
        'after_text_close': '</div>',  # marker for closing the production-pattern callout
        'callout': make_callout(
            'fun-note',
            'Fun Fact: Hybrid IE as hospital triage',
            'Cartoon hospital ER reception desk. A receptionist robot labeled spaCy stamps a clipboard CLEARED for a queue of routine patients. To the right, one patient with a question-mark thought bubble walks toward a tall wise wizard-doctor labeled LLM. A wall sign reads Hybrid IE Triage: 70% never reach the wizard.',
            'images/comic-hospital-triage.png',
            '<strong>Figure 34.3.3</strong>: The hybrid hospital. spaCy is the triage nurse who sends the routine cases home; the LLM is the specialist consulted only when the case is genuinely unusual.',
        ),
    },
    # ch34-2 SRL detective board: place after first paragraph of section
    {
        'file': 'part-7-retrieval-information-extraction-with-llms/module-34-structured-information-extraction-ner/section-34.2.html',
        'src': 'images/comic-srl-detective-board.png',
        'after_text': '<h2 id="34-2-1-classical-ner-with-spacy">34.2.1 Classical NER with spaCy</h2>',
        'callout': make_callout(
            'fun-note',
            'Fun Fact: Semantic Role Labeling as a whodunit',
            "A cozy detective's pinboard, sepia tones, with a magnifying glass and red string connecting labeled photo cards: AGENT butler, PATIENT lord, INSTRUMENT candlestick, LOCATION library, TEMPORAL 9pm. Above the board a chalkboard reads Semantic Role Labeling.",
            'images/comic-srl-detective-board.png',
            '<strong>Figure 34.2.2</strong>: Semantic Role Labeling tags who did what to whom, where, and when. Once a sentence has been SRL-tagged, the rest of the IE pipeline is a database insert away.',
        ),
    },
    # ch34-4 graceful degradation: at start of section
    {
        'file': 'part-7-retrieval-information-extraction-with-llms/module-34-structured-information-extraction-ner/section-34.4.html',
        'src': 'images/comic-graceful-degradation.png',
        'after_text': '<h2 id="34-4-5-grounding-verification">34.4.5 Grounding Verification</h2>',
        'callout': make_callout(
            'fun-note',
            'Fun Fact: Graceful degradation when the LLM is asleep',
            'Two cartoon characters wired by a glowing cable. On the left a small alert robot labeled spaCy is working. On the right a larger robot labeled LLM has a Z over its head, fast asleep, with an unplugged cable. A circuit-breaker switch between them is flipped to BYPASS.',
            'images/comic-graceful-degradation.png',
            '<strong>Figure 34.4.2</strong>: When the LLM service is down, the classical pipeline still ships entities. The application degrades to "classical-only mode" rather than failing the request entirely.',
        ),
    },
    # ch34-5 coreference pipeline mental-map
    {
        'file': 'part-7-retrieval-information-extraction-with-llms/module-34-structured-information-extraction-ner/section-34.5.html',
        'src': 'images/comic-coreference-pipeline.png',
        'after_text': '<h2 id="34-5-8-integrated-document-understanding-pipeline">34.5.8 Integrated Document Understanding Pipeline</h2>',
        'callout': make_callout(
            'key-insight',
            'Key Insight: The four-stage document understanding pipeline',
            'A cute assembly line cartoon where a single document passes through four conveyor stations labelled CO-REF, NER, RELATIONS, GRAPH. Four small robot workers each stamp it with their own tool. The output bin is labelled Knowledge Graph.',
            'images/comic-coreference-pipeline.png',
            '<strong>Figure 34.5.2</strong>: Coreference resolution, NER, relation extraction, and graph assembly form a pipeline that converts raw text into structured knowledge. Each stage adds one kind of annotation; the final output is a query-ready knowledge graph.',
        ),
    },
    # ch24-6 dexterity ceiling
    {
        'file': 'part-5-multimodal-llms/module-24-vla-models/section-24.6.html',
        'src': 'images/comic-dexterity-ceiling.png',
        'after_text': '<h2 id="24-6-2-the-dexterity-ceiling">24.6.2 The Dexterity Ceiling</h2>',
        'callout': make_callout(
            'fun-note',
            'Fun Fact: The dexterity ceiling, illustrated',
            "A friendly cartoon robot arm gleefully stacks apples in a pyramid. Right next to it, a single candy bar lies on the table; the robot's gripper hovers over it confused.",
            'images/comic-dexterity-ceiling.png',
            '<strong>Figure 24.6.2</strong>: Every modern VLA can pick the apple. Almost none of them can unwrap the candy bar. Dexterity is the line between "demo" and "production".',
        ),
    },
    # ch26-6 dialogue vs process memory
    {
        'file': 'part-6-agentic-ai/module-26-ai-agents/section-26.6.html',
        'src': 'images/comic-dialogue-vs-process-memory.png',
        'after_text': '<h2 id="26-6-1-what-is-agent-specific-about-agent-memory">26.6.1 What Is Agent-Specific About Agent Memory</h2>',
        'callout': make_callout(
            'fun-note',
            'Fun Fact: Dialogue memory on the left, process memory on the right',
            'A cartoon agent at a wooden desk. Left stack: tidy printed transcripts labelled Dialogue Memory. Right stack: chaotic sticky notes, todo lists, receipts labelled Process Memory. The agent picks one note from the right pile.',
            'images/comic-dialogue-vs-process-memory.png',
            '<strong>Figure 26.6.2</strong>: The cleanest mental separation. Dialogue memory is the user-facing transcript; process memory is the off-stage scratchpad of tool calls and sub-goals. Mix them at your peril.',
        ),
    },
    # ch35-2 cypher treasure map
    {
        'file': 'part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/section-35.2.html',
        'src': 'images/comic-cypher-treasure-map.png',
        'after_text': '<h2 id="35-2-3-cypher-queries-for-rag">35.2.3 Cypher Queries for RAG</h2>',
        'callout': make_callout(
            'fun-note',
            'Fun Fact: A Cypher query as a treasure-hunt map',
            "An old treasure-hunt map with nodes labelled like Wikipedia stubs ('Einstein', 'Ulm', 'Germany'), and a dotted line traversing them. A pirate-themed cartoon traveler follows the dots.",
            'images/comic-cypher-treasure-map.png',
            '<strong>Figure 35.2.5</strong>: A Cypher MATCH clause is a treasure map: declare the node pattern, declare the edge pattern, and the engine traces the route through the graph.',
        ),
    },
    # ch37-3 lost in the middle
    {
        'file': 'part-8-conversational-ai-with-llms/module-37-conversational-ai/section-37.3.html',
        'src': 'images/comic-lost-in-the-middle.png',
        'after_text': '<h2 id="37-3-2-the-lost-in-the-middle-effect">37.3.2 The Lost-in-the-Middle Effect</h2>',
        'callout': make_callout(
            'fun-note',
            'Fun Fact: The lost-in-the-middle bench',
            'A long park bench with many people sitting on it. The two ends (recent + oldest) are well-lit. The middle is in shadow, with question marks over their heads. An LLM character at one end says "I can hear the ends just fine".',
            'images/comic-lost-in-the-middle.png',
            '<strong>Figure 37.3.4</strong>: The lost-in-the-middle effect. Most LLMs attend strongly to the beginning and end of long contexts and patchily to the middle. Order matters; place the load-bearing facts at the edges.',
        ),
    },
    # ch41-2 goldfish memory  (section-41.2 is NOT touched by agent 5)
    {
        'file': 'part-8-conversational-ai-with-llms/module-41-conv-ai-tools/section-41.2.html',
        'src': 'images/comic-goldfish-memory.png',
        'after_text': '<h2 id="41-2-1-conversation-memory-primitives">41.2.1 Conversation memory primitives</h2>',
        'callout': make_callout(
            'fun-note',
            'Fun Fact: The chatbot with a goldfish on its head',
            'A friendly chatbot robot with a literal goldfish in a small fishbowl balanced on its head, trying hard to remember something. Speech bubble: "something about a dog?"',
            'images/comic-goldfish-memory.png',
            '<strong>Figure 41.2.2</strong>: Most chatbots remember by accident. Real conversation memory is short-term (in hand), medium-term (on the hook), and long-term (in the user profile).',
        ),
    },
    # ch41-2 framework graveyard
    {
        'file': 'part-8-conversational-ai-with-llms/module-41-conv-ai-tools/section-41.2.html',
        'src': 'images/comic-framework-graveyard.png',
        'after_text': '<h2 id="41-2-2-framework-half-life">41.2.2 Framework half-life</h2>',
        'callout': make_callout(
            'fun-note',
            'Fun Fact: The LangChain abstractions cemetery',
            'A small cartoon cemetery in autumn. Three small tombstones labelled Chains, LCEL, AgentExecutor. Next to them a fresh sapling with a sign LangGraph 2024. A gardener-robot waters it.',
            'images/comic-framework-graveyard.png',
            '<strong>Figure 41.2.3</strong>: Framework half-life is ~18 months. Pin the API surface you actually use; the abstractions above it will get renamed at least once before your roadmap ships.',
        ),
    },
    # ch59-2 ZeRO mountain climbers (section-59.2 is NOT touched by agent 5)
    {
        'file': 'part-12-llm-systems-at-scale/module-59-distributed-training-systems/section-59.2.html',
        'src': 'images/comic-zero-mountain-climbers.png',
        'after_text': '<h2 id="59-2-2-the-zero-progression">59.2.2 The ZeRO Progression</h2>',
        'callout': make_callout(
            'fun-note',
            'Fun Fact: ZeRO climbers, each carrying less',
            "A vertical mountain climb scene. Four cartoon climbers progressing upward, labelled Stage 0, Stage 1, Stage 2, Stage 3. Each carries a smaller backpack than the one below. The summit is labelled Trillion-parameter model.",
            'images/comic-zero-mountain-climbers.png',
            '<strong>Figure 59.2.2</strong>: ZeRO climbers ascend the memory mountain. Stage 0 carries everything; Stage 3 carries just a daypack. The trade is communication for memory: higher stages talk to peers more often.',
        ),
    },
]


def fix():
    n_inserted = 0
    n_skipped = 0
    n_no_anchor = 0
    for ins in INSERTIONS:
        path = ROOT / ins['file']
        if not path.exists():
            print(f'  SKIP (no file): {ins["file"]}')
            continue
        text = path.read_text(encoding='utf-8')
        # Idempotent: skip if image already referenced
        if ins['src'] in text:
            n_skipped += 1
            continue
        # Find anchor and insert AFTER it (newline after anchor)
        anchor = ins['after_text']
        idx = text.find(anchor)
        if idx == -1:
            n_no_anchor += 1
            print(f'  NO ANCHOR in {ins["file"]}: anchor={anchor[:60]!r}')
            continue
        # Find the next newline after the anchor (insert after the line that contains the anchor)
        line_end = text.find('\n', idx + len(anchor))
        if line_end == -1:
            line_end = idx + len(anchor)
        insertion_pt = line_end + 1
        new_text = text[:insertion_pt] + ins['callout'] + text[insertion_pt:]
        path.write_text(new_text, encoding='utf-8')
        n_inserted += 1
        print(f'  WIRED {ins["src"]} -> {ins["file"]}')
    print(f'\nWired {n_inserted} comic callouts; skipped {n_skipped} (already present); {n_no_anchor} anchors not found')


if __name__ == '__main__':
    fix()
