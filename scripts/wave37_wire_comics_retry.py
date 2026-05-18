"""Wave 37 retry: wire the 5 comic callouts whose anchors didn't match.

Anchors found via grep of actual h2 IDs in each file.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from wave37_wire_comics import make_callout

ROOT = Path(__file__).resolve().parents[1]

INSERTIONS = [
    # 34.2: SRL detective board — use the Open IE section as anchor
    {
        'file': 'part-7-retrieval-information-extraction-with-llms/module-34-structured-information-extraction-ner/section-34.2.html',
        'src': 'images/comic-srl-detective-board.png',
        'after_text': '<h2 id="34-2-3-open-information-extraction">34.2.3 Open Information Extraction</h2>',
        'callout': make_callout(
            'fun-note',
            'Fun Fact: Semantic Role Labeling as a whodunit',
            "A cozy detective's pinboard, sepia tones, with a magnifying glass and red string connecting labeled photo cards: AGENT butler, PATIENT lord, INSTRUMENT candlestick, LOCATION library, TEMPORAL 9pm. Above the board a chalkboard reads Semantic Role Labeling.",
            'images/comic-srl-detective-board.png',
            '<strong>Figure 34.2.2</strong>: Semantic Role Labeling tags who did what to whom, where, and when. Once a sentence has been SRL-tagged, the rest of the IE pipeline is a database insert away.',
        ),
    },
    # 34.4: graceful degradation — use Production Deployment Patterns as anchor
    {
        'file': 'part-7-retrieval-information-extraction-with-llms/module-34-structured-information-extraction-ner/section-34.4.html',
        'src': 'images/comic-graceful-degradation.png',
        'after_text': '<h2 id="34-4-5-production-deployment-patterns">34.4.5 Production Deployment Patterns</h2>',
        'callout': make_callout(
            'fun-note',
            'Fun Fact: Graceful degradation when the LLM is asleep',
            'Two cartoon characters wired by a glowing cable. On the left a small alert robot labeled spaCy is working. On the right a larger robot labeled LLM has a Z over its head, fast asleep, with an unplugged cable. A circuit-breaker switch between them is flipped to BYPASS.',
            'images/comic-graceful-degradation.png',
            '<strong>Figure 34.4.2</strong>: When the LLM service is down, the classical pipeline still ships entities. The application degrades to "classical-only mode" rather than failing the request entirely.',
        ),
    },
    # 35.2: Cypher treasure map — use Cypher-Based Multi-Hop Retrieval as anchor
    {
        'file': 'part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/section-35.2.html',
        'src': 'images/comic-cypher-treasure-map.png',
        'after_text': '<h2 id="35-2-4-cypher-based-multi-hop-retrieval">35.2.4 Cypher-Based Multi-Hop Retrieval</h2>',
        'callout': make_callout(
            'fun-note',
            'Fun Fact: A Cypher query as a treasure-hunt map',
            "An old treasure-hunt map with nodes labelled like Wikipedia stubs ('Einstein', 'Ulm', 'Germany'), and a dotted line traversing them. A pirate-themed cartoon traveler follows the dots.",
            'images/comic-cypher-treasure-map.png',
            '<strong>Figure 35.2.5</strong>: A Cypher MATCH clause is a treasure map: declare the node pattern, declare the edge pattern, and the engine traces the route through the graph.',
        ),
    },
    # 37.3: lost-in-middle — use Short-Term Memory Strategies as anchor (relevant context)
    {
        'file': 'part-8-conversational-ai-with-llms/module-37-conversational-ai/section-37.3.html',
        'src': 'images/comic-lost-in-the-middle.png',
        'after_text': '<h2 id="37-3-2-short-term-memory-strategies">37.3.2 Short-Term Memory Strategies</h2>',
        'callout': make_callout(
            'fun-note',
            'Fun Fact: The lost-in-the-middle bench',
            'A long park bench with many people sitting on it. The two ends (recent + oldest) are well-lit. The middle is in shadow, with question marks over their heads. An LLM character at one end says "I can hear the ends just fine".',
            'images/comic-lost-in-the-middle.png',
            '<strong>Figure 37.3.4</strong>: The lost-in-the-middle effect. Most LLMs attend strongly to the beginning and end of long contexts and patchily to the middle. Order matters; place the load-bearing facts at the edges.',
        ),
    },
    # 41.2: framework graveyard — use Conversation Orchestration Frameworks as anchor
    {
        'file': 'part-8-conversational-ai-with-llms/module-41-conv-ai-tools/section-41.2.html',
        'src': 'images/comic-framework-graveyard.png',
        'after_text': '<h2 id="41-2-2-conversation-orchestration-frameworks">41.2.2 Conversation orchestration frameworks</h2>',
        'callout': make_callout(
            'fun-note',
            'Fun Fact: The LangChain abstractions cemetery',
            'A small cartoon cemetery in autumn. Three small tombstones labelled Chains, LCEL, AgentExecutor. Next to them a fresh sapling with a sign LangGraph 2024. A gardener-robot waters it.',
            'images/comic-framework-graveyard.png',
            '<strong>Figure 41.2.3</strong>: Framework half-life is ~18 months. Pin the API surface you actually use; the abstractions above it will get renamed at least once before your roadmap ships.',
        ),
    },
]


def main():
    n_inserted = 0
    for ins in INSERTIONS:
        path = ROOT / ins['file']
        text = path.read_text(encoding='utf-8')
        if ins['src'] in text:
            print(f'  SKIP (already): {ins["src"]}')
            continue
        anchor = ins['after_text']
        idx = text.find(anchor)
        if idx == -1:
            print(f'  NO ANCHOR: {anchor[:60]!r}')
            continue
        line_end = text.find('\n', idx + len(anchor))
        if line_end == -1:
            line_end = idx + len(anchor)
        insertion_pt = line_end + 1
        new_text = text[:insertion_pt] + ins['callout'] + text[insertion_pt:]
        path.write_text(new_text, encoding='utf-8')
        n_inserted += 1
        print(f'  WIRED {ins["src"]}')
    print(f'\nRetry wired {n_inserted} callouts')


if __name__ == '__main__':
    main()
