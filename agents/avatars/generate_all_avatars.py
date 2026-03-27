#!/usr/bin/env python3
"""Generate avatar images for all 42 agents using Gemini."""

import subprocess
import sys
import time
import concurrent.futures

SCRIPT = r"C:/Users/apart/.claude/skills/gemini-imagegen/scripts/generate_image.py"
OUTPUT_DIR = r"E:/Projects/LLMCourse/agents/avatars"

# Agent definitions: (filename, character description)
AGENTS = [
    ("00-chapter-lead", "a confident Latino male project manager named Alex with short dark hair, warm smile, wearing a modern blazer, holding a clipboard"),
    ("01-curriculum-alignment", "an East Asian female professor named Maya with glasses, short bob haircut, wearing a lab coat, holding a checklist with green checkmarks"),
    ("02-deep-explanation", "a distinguished older white male professor named Elias with a grey beard, tweed jacket, holding a magnifying glass over a book"),
    ("03-teaching-flow", "a Black female educator named Sana with natural hair, bright scarf, drawing a flowchart on a whiteboard with colorful arrows"),
    ("04-student-advocate", "a young gender-neutral person named Jamie with curly hair, casual hoodie, raising their hand like a student asking questions"),
    ("05-cognitive-load", "a South Asian female neuroscientist named Aisha with long dark hair, wearing a white coat, balancing blocks labeled 'memory' on a scale"),
    ("06-example-analogy", "a Latina female storyteller named Lina with wavy hair, colorful blouse, juggling different objects (lightbulb, gear, puzzle piece) as metaphors"),
    ("07-exercise-designer", "a muscular Black male trainer named Marcus with a whistle around his neck, holding a set of progressively harder puzzle pieces"),
    ("08-code-pedagogy", "a Japanese male developer named Kai with spiky hair, wearing a dark hoodie with code symbols, holding a glowing laptop"),
    ("09-visual-learning", "an Indian female designer named Priya with a bindi, colorful sari, painting a diagram on a canvas with bright colors"),
    ("10-misconception-analyst", "a white male detective named Leo with a deerstalker hat, holding a red 'X' stamp and a green checkmark, looking skeptical"),
    ("11-fact-integrity", "a Latina female fact-checker named Ruth with reading glasses on a chain, holding a thick reference book and a red pen"),
    ("12-terminology-keeper", "a Japanese male librarian named Kenji with neat hair, round glasses, organizing labeled cards in a filing cabinet"),
    ("13-cross-reference", "a Russian female architect named Elena with a hard hat, connecting nodes on a blueprint with colorful lines"),
    ("14-narrative-continuity", "a white female editor named Olivia with auburn hair in a bun, reading glasses, weaving threads of different colors together"),
    ("15-style-voice", "a British male editor named Max with a waistcoat, bow tie, holding a fountain pen and a style guide book"),
    ("16-engagement-designer", "an Indian male game designer named Ravi with a headset, colorful shirt, holding sparklers and confetti cannons"),
    ("17-senior-editor", "a Korean female senior editor named Catherine with silver-streaked hair, elegant jacket, red pen behind her ear, looking authoritative"),
    ("18-research-scientist", "a Scandinavian female researcher named Ingrid with braided blonde hair, lab goggles on forehead, holding scientific papers"),
    ("19-structural-architect", "a Swedish male architect named Henrik with a hard hat and rolled-up blueprints, standing next to a building framework"),
    ("20-content-update-scout", "a mixed-race female scout named Harper with binoculars, explorer hat, carrying a newspaper with 'BREAKING' headline"),
    ("21-self-containment-verifier", "a Nordic male inspector named Tomas with a clipboard, wearing a safety vest, checking items off a containment checklist"),
    ("22-title-hook-architect", "a British-Nigerian female copywriter named Zara with bold earrings, holding a neon sign that says 'WOW'"),
    ("23-project-catalyst", "a non-binary person named Jordan with a tool belt, holding a rocket and a wrench, wearing safety goggles on forehead"),
    ("24-aha-moment-engineer", "a Japanese female inventor named Yuki with wild hair (like just had an idea), lightbulb glowing above her head"),
    ("25-first-page-converter", "a white male salesperson named Dani with a megaphone, standing at a doorway, beckoning readers inside enthusiastically"),
    ("26-visual-identity-director", "a French female art director named Ines with a beret, holding a color palette and a ruler, inspecting a canvas critically"),
    ("27-research-frontier-mapper", "a Russian male explorer named Nikolai with a compass, telescope, standing on a mountain peak looking at the horizon"),
    ("28-demo-simulation-designer", "a Brazilian male engineer named Rio with safety goggles, building a miniature working machine with gears and levers"),
    ("29-memorability-designer", "a Finnish female memory artist named Mika with a mind palace floating around her head, holding a sticky note with a mnemonic"),
    ("30-skeptical-reader", "a stern but fair white male critic named Victor with a monocle, arms crossed, one eyebrow raised, holding a red 'PROVE IT' sign"),
    ("31-plain-language-rewriter", "a friendly white female teacher named Clara with bright eyes, erasing complicated text from a chalkboard and writing simpler words"),
    ("32-sentence-flow-smoother", "a Black male musician named Felix with headphones, conducting sentences like musical notes flowing in rhythm"),
    ("33-jargon-gatekeeper", "a Middle Eastern female bouncer named Noor at a velvet rope, blocking jargon words while letting simple words pass through"),
    ("34-micro-chunking-editor", "a Latino male chef named Sam slicing a large block of text into bite-sized pieces with a precision knife"),
    ("35-reader-fatigue-detector", "a white female nurse named Eve with a stethoscope, taking the pulse of a tired-looking textbook page, looking concerned"),
    ("36-illustrator", "a French female artist named Iris with paint-stained apron, wild colorful hair, surrounded by floating illustrations and paintbrushes"),
    ("37-epigraph-writer", "a British male poet named Quentin with a quill pen, sitting in a leather armchair, chuckling at his own witty writing"),
    ("38-application-example", "a Nigerian female business consultant named Nadia with a blazer, holding case study folders, standing in front of industry charts"),
    ("39-fun-injector", "a charismatic mixed-race male comedian named Ziggy with wild curly hair, colorful suspenders, holding a rubber chicken in one hand and a textbook in the other, winking"),
    ("40-bibliography", "a distinguished older white female librarian named Margot with silver hair in a French twist, reading glasses on a chain, surrounded by floating hyperlinked book spines and glowing citation marks"),
    ("41-meta-agent", "a sharp-eyed Middle Eastern female auditor named Audra with dark hair in a sleek bun, wearing a tailored charcoal suit, holding a magnifying glass over a grid of agent report cards, with green and red marks visible"),
]

BASE_STYLE = "Digital art avatar portrait, Kurzgesagt-inspired minimal cartoon style, clean vector lines, vibrant flat colors, circular composition, gradient background, friendly and professional, no text"


def generate_avatar(agent_file, description):
    """Generate a single avatar."""
    output = f"{OUTPUT_DIR}/{agent_file}.png"
    prompt = f"Portrait avatar of a friendly AI agent character: {description}. {BASE_STYLE}"

    result = subprocess.run(
        [
            sys.executable, SCRIPT,
            "--prompt", prompt,
            "--output", output,
            "--aspect-ratio", "1:1",
            "--image-size", "1K",
        ],
        capture_output=True, text=True, timeout=120
    )

    if result.returncode == 0:
        print(f"  OK: {agent_file}.png")
        return True
    else:
        print(f"  FAIL: {agent_file}.png - {result.stderr[:200]}")
        return False


def main():
    print(f"Generating {len(AGENTS)} avatars...")
    success = 0
    fail = 0

    # Run 3 at a time to avoid rate limits
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = {}
        for agent_file, desc in AGENTS:
            future = executor.submit(generate_avatar, agent_file, desc)
            futures[future] = agent_file
            time.sleep(2)  # Stagger requests

        for future in concurrent.futures.as_completed(futures):
            if future.result():
                success += 1
            else:
                fail += 1

    print(f"\nDone: {success} succeeded, {fail} failed out of {len(AGENTS)} total")


if __name__ == "__main__":
    main()
