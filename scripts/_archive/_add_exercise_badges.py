"""
Add exercise-type badge spans to all exercise callouts across 23 HTML files.
Classifies each exercise as: conceptual, coding, analysis, or discussion.
"""
import re
import os

# All files to process
FILES = [
    "part-3-working-with-llms/module-10-llm-apis/section-10.4.html",
    "part-3-working-with-llms/module-11-prompt-engineering/section-11.5.html",
    "part-5-retrieval-conversation/module-19-embeddings-vector-db/section-19.1.html",
    "part-5-retrieval-conversation/module-19-embeddings-vector-db/section-19.2.html",
    "part-5-retrieval-conversation/module-19-embeddings-vector-db/section-19.3.html",
    "part-5-retrieval-conversation/module-19-embeddings-vector-db/section-19.4.html",
    "part-5-retrieval-conversation/module-19-embeddings-vector-db/section-19.5.html",
    "part-5-retrieval-conversation/module-20-rag/section-20.1.html",
    "part-5-retrieval-conversation/module-20-rag/section-20.2.html",
    "part-5-retrieval-conversation/module-20-rag/section-20.3.html",
    "part-5-retrieval-conversation/module-20-rag/section-20.4.html",
    "part-5-retrieval-conversation/module-20-rag/section-20.5.html",
    "part-5-retrieval-conversation/module-20-rag/section-20.6.html",
    "part-5-retrieval-conversation/module-21-conversational-ai/section-21.1.html",
    "part-5-retrieval-conversation/module-21-conversational-ai/section-21.2.html",
    "part-5-retrieval-conversation/module-21-conversational-ai/section-21.3.html",
    "part-5-retrieval-conversation/module-21-conversational-ai/section-21.4.html",
    "part-5-retrieval-conversation/module-21-conversational-ai/section-21.5.html",
    "part-10-frontiers/module-34-emerging-architectures/section-34.1.html",
    "part-10-frontiers/module-34-emerging-architectures/section-34.2.html",
    "part-10-frontiers/module-35-ai-society/section-35.1.html",
    "part-10-frontiers/module-35-ai-society/section-35.2.html",
    "part-10-frontiers/module-35-ai-society/section-35.3.html",
]

BASE = r"E:\Projects\LLMCourse"


def classify_exercise(title_text, body_text):
    """Classify an exercise based on title and body content.

    Strategy: check for strong signals in priority order.
    The first sentence of the exercise body is the most reliable indicator.
    """
    combined = (title_text + " " + body_text).lower()
    plain = re.sub(r'<[^>]+>', ' ', combined)
    # Get the first ~300 chars (the prompt/instruction part, before any answer)
    first_part = plain[:400]

    # Check if the title already has a type hint in parentheses (part-10 files)
    title_type_match = re.search(r'\((Analysis|Discussion|Coding|Conceptual|Reflection)\)', title_text, re.IGNORECASE)
    if title_type_match:
        t = title_type_match.group(1).lower()
        if t == 'reflection':
            return 'discussion'
        return t

    # ============================================================
    # CONCEPTUAL: The exercise asks you to explain/describe/reason about concepts
    # Key signal: imperative verbs like "explain", "describe", "what happens if"
    # and NO requirement to actually write/run code
    # ============================================================
    conceptual_patterns = [
        r'^.*?explain\s+(why|how|what|the\b)',
        r'^.*?describe\s+(two|three|the|how|what|a\b)',
        r'^.*?what\s+(happens|problems?|would happen|is the (difference|purpose|role|advantage))',
        r'^.*?why\s+(is|does|do|would|might|are|can)\b',
        r'^.*?in\s+your\s+own\s+words',
        r'^.*?under\s+what\s+conditions?\b',
        r'^.*?what\s+(are|is)\s+the\s+(tradeoffs?|advantages?|disadvantages?|limitations?|challenges?)',
        r'^.*?how\s+does\b.*\b(address|solve|help|work|differ|affect)\b',
        r'^.*?what\s+role\b',
        r'^.*?compare\s+and\s+contrast\b',
        r'^.*?when\s+does\b.*\b(help|hurt|fail|break|work)\b',
        r'^.*?when\s+would\s+you\b',
    ]

    # ============================================================
    # CODING: The exercise asks you to write/run actual code
    # Key signal: use a library, implement X, build Y, write code
    # ============================================================
    coding_patterns = [
        r'use\s+<code>',            # "Use <code>sentence-transformers</code>"
        r'using\s+<code>',          # "Using <code>..."
        r'using\s+(the\s+)?<code>',
        r'\bimplement\b',           # "Implement a ..."
        r'\bbuild\b.*\b(pipeline|system|function|bot|prototype|chain|wrapper|handler)',
        r'\bwrite\b.*\b(code|function|script|program|class|handler)',
        r'\bcreate\b.*\b(script|function|pipeline|class|module|program|tool|index|prototype)',
        r'\bconstruct\b.*\b(api|call|request|pipeline|query)',
        r'\bextend\b.*\b(abstraction|wrapper|class|function|system)',
        r'\bdeploy\b',
        r'\bconfigure\b.*\b(the|your|a)\b',
        r'\bfine[- ]tune\b.*\b(a |the |your |an )',  # "Fine-tune a model"
        r'\bset\s+up\b',
        r'\bstreaming\s+handler\b',
        r'\bfallback\b.*\b(mechanism|strategy|chain)\b.*\b(implement|build|add|create)',
    ]

    # Also coding if body has <code> tags AND action verbs
    has_code_tag = '<code>' in body_text
    code_action_with_lib = has_code_tag and re.search(
        r'\b(embed|compute|store|query|index|chunk|load|insert|retrieve|measure|compare|test|record|send|call|take|plot|visualize)\b',
        first_part, re.IGNORECASE
    )

    # ============================================================
    # ANALYSIS: analyze data, evaluate, benchmark, calculate, compare outputs
    # ============================================================
    analysis_patterns = [
        r'\banalyz[ei]\b',
        r'\bcalculat[ei]\b',
        r'\bbenchmark\b',
        r'\bquantif[yi]\b',
        r'\bevaluat[ei]\s+(the\s+)?(results?|outputs?|performance|quality|impact|effectiveness)',
        r'\bmeasure\s+the\b',
        r'\bcompare\s+(the\s+)?(outputs?|results?|performance|quality)',
        r'\brun\s+(an?\s+)?experiment',
        r'\bassessment\b',
    ]

    # ============================================================
    # DISCUSSION: debate, implications, ethics, open-ended, propose strategy
    # ============================================================
    discussion_patterns = [
        r'\bdiscuss\b.*\b(implication|impact|consequence|role)',
        r'\bdebate\b',
        r'\bargue\s+(for|against|whether|that)\b',
        r'\bpropose\b.*\b(solution|approach|strategy|framework|design)',
        r'\bdesign\b.*\b(strategy|protocol|framework|approach|roadmap|plan)\b',
        r'\bwhat\b.*\bshould\b.*\b(the|your|we|you|a)\b',
        r'\blist\s+at\s+least\b.*\b(explanation|alternative|reason)',
        r'\bwhat\s+(additional\s+)?experiments?\s+would\s+you\b',
        r'\bhow\s+would\s+you\s+design\b',
        r'\b(ethical|governance|implications)\b',
        r'\broadmap\b',
        r'\breflection\b',
    ]

    def score_patterns(patterns, text):
        count = 0
        for p in patterns:
            if re.search(p, text, re.IGNORECASE):
                count += 1
        return count

    # Score each category
    c_concept = score_patterns(conceptual_patterns, first_part)
    c_coding = score_patterns(coding_patterns, body_text)  # Use raw HTML for <code> detection
    c_analysis = score_patterns(analysis_patterns, first_part)
    c_discussion = score_patterns(discussion_patterns, first_part)

    # Boost coding if there's code_action_with_lib
    if code_action_with_lib:
        c_coding += 2

    # If the exercise starts with "Explain why/how" or "Describe", that's a very strong conceptual signal
    # Override coding unless there's an explicit "implement/build/write code" instruction
    strong_conceptual = bool(re.search(
        r'(explain\s+(why|how|what|the)|describe\s+(two|three|the|how)|what\s+(happens|problems|would)|why\s+(is|does|do|would|might|are)|when\s+does\b.*\b(help|hurt|fail|break|work))',
        first_part, re.IGNORECASE
    ))
    # Only check the exercise prompt text (before <details>) for strong coding signals
    prompt_text = body_text.split('<details>')[0] if '<details>' in body_text else body_text[:500]
    strong_coding = bool(re.search(
        r'(implement\s+(a|the|an|your)\b|build\s+a|write\s+(a|code|the)|create\s+a|'
        r'use\s+<code>|using\s+<code>|using\s+the\s+<code>|fine[- ]tune\s+a|'
        r'use\s+[A-Z]\w+\s+(on|to)\b|take\s+a\s+model\b)',
        prompt_text, re.IGNORECASE
    )) or code_action_with_lib

    # Hands-on experiment detection (send API calls, record results, try settings)
    hands_on = bool(re.search(
        r'\b(send\s+(it|the|a|this|the same)|record\s+the|try\s+(with|different|three|two)|'
        r'test\s+with\b.*\b(query|prompt|input)|'
        r'pick\s+a\s+task|using\s+any\b.*\bapi\b|'
        r'compare\s+the\s+(quality|cost|latency|response|output)|'
        r'observe\s+(the|how|what))\b',
        first_part, re.IGNORECASE
    ))

    # Decision logic
    if strong_conceptual and not strong_coding and not hands_on:
        return 'conceptual'

    if strong_coding:
        return 'coding'

    if hands_on:
        return 'coding'

    # If both or neither, use scores
    scores = {
        'conceptual': c_concept,
        'coding': c_coding,
        'analysis': c_analysis,
        'discussion': c_discussion,
    }

    max_score = max(scores.values())
    if max_score == 0:
        if has_code_tag:
            return 'coding'
        return 'conceptual'

    # Return highest, with tie-breaking priority
    for cat in ['coding', 'analysis', 'discussion', 'conceptual']:
        if scores[cat] == max_score:
            return cat

    return 'conceptual'


def extract_exercise_body(html, start_pos):
    """Extract the HTML content of the current exercise callout only.
    Stops at the next closing </div> that ends the callout, or the next exercise."""
    chunk = html[start_pos:start_pos + 3000]
    # Find the end of the current exercise: next <div class="callout exercise"> or </section>
    end_markers = [
        r'<div class="callout exercise">',
        r'<div class="callout\b',
        r'</section>',
        r'<div class="whats-next"',
    ]
    earliest = len(chunk)
    for marker in end_markers:
        m = re.search(marker, chunk[10:])  # skip a bit to avoid matching self
        if m:
            earliest = min(earliest, m.start() + 10)
    return chunk[:earliest]


def process_file(filepath):
    """Process a single HTML file, adding exercise-type badges."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove any existing exercise-type badges (for idempotent re-runs)
    content = re.sub(r'\s*<span class="exercise-type \w+" title="\w+">\w+</span>', '', content)

    # Find all exercise callout-title lines
    pattern = r'(<div class="callout-title">Exercise\s+[\d.]+:\s*.*?)(</div>)'

    matches = list(re.finditer(pattern, content))
    if not matches:
        print(f"  NO EXERCISES: {filepath}")
        return 0

    count = 0
    for match in reversed(matches):
        title_content = match.group(1)

        # Extract exercise body for classification
        body_text = extract_exercise_body(content, match.end())
        title_text = re.sub(r'<[^>]+>', '', title_content)

        # Classify
        ex_type = classify_exercise(title_text, body_text)

        # Create the badge span
        type_label = ex_type.capitalize()
        badge = f' <span class="exercise-type {ex_type}" title="{type_label}">{type_label}</span>'

        # Insert before </div>
        insert_pos = match.end() - len('</div>')
        content = content[:insert_pos] + badge + content[insert_pos:]
        count += 1

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  Added {count} badges: {os.path.basename(filepath)}")
    return count


def main():
    total = 0
    file_count = 0

    for rel_path in FILES:
        filepath = os.path.join(BASE, rel_path)
        if not os.path.exists(filepath):
            print(f"  FILE NOT FOUND: {filepath}")
            continue

        file_count += 1
        n = process_file(filepath)
        total += n

    print(f"\nTotal: {total} exercise badges added across {file_count} files")


if __name__ == '__main__':
    main()
