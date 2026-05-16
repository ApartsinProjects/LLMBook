#!/usr/bin/env python
"""Generate all 25 missing visual assets via Gemini concurrent generation.

REGENERATE: 20 broken images from the queue (high pedagogy hero illustrations).
HERO GAPS: 5 missing hero illustrations for Appendices O-S.

Style: Warm cartoon-style, Kurzgesagt-meets-XKCD, friendly characters,
clear iconography, soft palette, 16:9 aspect for chapter openers.
"""
from __future__ import annotations

import concurrent.futures
import json
import sys
import time
from pathlib import Path

from google import genai
from google.genai import types

CONFIG = json.loads(Path.home().joinpath(".gemini-imagegen.json").read_text())
CLIENT = genai.Client(api_key=CONFIG["api_key"])
MODEL = "gemini-3.1-flash-image-preview"

ROOT = Path("E:/Projects/BookBlogsHome/LLMBook")

STYLE = (
    "Warm cartoon-style hero illustration, Kurzgesagt-meets-XKCD aesthetic, "
    "friendly cartoon characters with simple expressive faces, clear iconography, "
    "soft pastel palette of teals, warm yellows, friendly oranges, soft pinks. "
    "Clean vector-feel shading. Avoid photorealism, avoid any visible text or "
    "letters or numbers in the image (they always render incorrectly)."
)

# Each entry: (output_path_relative_to_ROOT, subject_prompt, aspect)
JOBS: list[tuple[str, str, str]] = [
    # ---- HERO GAPS (5) ----
    (
        "appendices/appendix-o-course-syllabi/images/chapter-opener.png",
        "Five robot students sitting at classroom desks, each wearing a "
        "different colored graduation cap (blue, red, green, yellow, orange). "
        "Instructor robot at a chalkboard pointing at a branching tree diagram "
        "showing five tracks growing out of a shared foundation trunk. Each "
        "branch is a different color matching the students' caps. Cozy classroom "
        "with hanging plants and a window.",
        "16:9",
    ),
    (
        "appendices/appendix-p-reading-pathways/images/chapter-opener.png",
        "A friendly robot hiker standing at a forest trailhead with eight wooden "
        "signposts pointing different directions, each signpost decorated with a "
        "small symbol (book, gear, microscope, palette, etc). The trails branch "
        "out across a colorful hillside in autumn. The robot holds a folded trail "
        "map and looks contemplative.",
        "16:9",
    ),
    (
        "appendices/appendix-q-intermediate-projects/images/chapter-opener.png",
        "Three small robot apprentices each standing on a step-stool of different "
        "height (small, medium, taller) in front of a workshop bench. Between a "
        "tiny 'lab' building on the left and a tall 'capstone' tower on the "
        "right. Each apprentice holds a different small project artifact. Warm "
        "workshop lighting.",
        "16:9",
    ),
    (
        "appendices/appendix-r-capstone-project/images/chapter-opener.png",
        "Three robot students standing on three differently-shaped podium "
        "platforms (full-stack platform with dashboards behind, API-only podium "
        "with cloud icons, research replication podium with paper-shaped "
        "trophy). Each robot holds a trophy of a different shape. Bright "
        "celebratory backdrop.",
        "16:9",
    ),
    (
        "appendices/appendix-s-war-stories/images/chapter-opener.png",
        "A robot detective in a trench coat standing in front of a cork bulletin "
        "board pinned with five rectangular newspaper clippings. Red string "
        "connects the clippings to small chapter-number tags pinned on the side. "
        "Soft desk lamp lighting the board. The detective points at one clipping "
        "with a magnifying glass.",
        "16:9",
    ),
    # ---- REGENERATE: 20 broken images ----
    (
        "appendices/appendix-e-orchestration-frameworks/images/chapter-opener.png",
        "A bustling marketplace of small tool stalls, each stall holding a "
        "different small icon (gear, chain link, flask, agent robot). Customers "
        "(robots and humans) wander between stalls comparing wares. Banners and "
        "awnings overhead. Sense of 2026 LLM tooling abundance.",
        "16:9",
    ),
    (
        "part-10-idea-to-product/module-41-product-management/images/product-management-juggling.png",
        "A friendly product manager robot juggling four spinning plates on "
        "sticks labeled with tiny icons (clock, star, dollar, target). The robot "
        "stands on a thin tightrope stretched between two cartoon office "
        "buildings. The buildings represent technical feasibility and business "
        "value. Soft cityscape behind.",
        "16:9",
    ),
    (
        "part-10-idea-to-product/module-42-strategy-prioritization/images/strategy-use-case-funnel.png",
        "A cartoon executive robot in a tie pouring many colorful use-case-idea "
        "balls (each a different bright color) into a large blue funnel. Only "
        "two polished gem-shaped objects emerge from the bottom of the funnel "
        "into a small wooden crate. Sense of strategic filtering.",
        "16:9",
    ),
    (
        "part-10-idea-to-product/module-42-strategy-prioritization/images/vendor-evaluation-market.png",
        "A small cartoon robot buyer with a shopping basket comparing three "
        "vendor booths at an outdoor market. Each booth has a different vendor "
        "robot: one with a giant model glowing behind it, one with a small "
        "speedy model, one with a toolkit hanging on hooks. Friendly stripes on "
        "the awnings.",
        "16:9",
    ),
    (
        "part-10-idea-to-product/module-43-vibe-coding/images/pair-programming-robot.png",
        "A small friendly robot sitting beside a human programmer at a desk, "
        "both looking at the same large monitor showing colored code blocks. "
        "Coffee mug for the human, oil can for the robot. Cozy desk lamp "
        "lighting, plants in the background.",
        "16:9",
    ),
    (
        "part-10-idea-to-product/module-46-compute-planning/images/compute-planning-blueprint.png",
        "A friendly robot architect with a tiny hard hat examining unfolded "
        "blueprints on a drafting table. GPU cards drawn as colorful building "
        "blocks stacked beside the blueprints in three sizes (small, medium, "
        "large). A calculator and dollar-sign chips sit on the corner of the "
        "table.",
        "16:9",
    ),
    (
        "part-10-idea-to-product/module-46-compute-planning/images/enterprise-integration-plumbing.png",
        "A large cartoon enterprise building with many small doors and "
        "keyhole windows. A friendly robot plumber on a ladder carefully "
        "connecting colored pipes and cables between different sections of the "
        "building. An identity-badge icon and a lock icon float beside the "
        "scene.",
        "16:9",
    ),
    (
        "part-10-idea-to-product/module-47-scaling-economics/images/roi-measurement-balance.png",
        "A cartoon accountant robot with round glasses sitting at a desk, "
        "operating an abacus with one hand and a calculator with the other. "
        "Coins flow off the desk on the left (cost side); golden stars float "
        "upward on the right (value side). A small balance scale sits in the "
        "middle.",
        "16:9",
    ),
    (
        "part-10-idea-to-product/module-47-scaling-economics/images/economic-design-token-kitchen.png",
        "A cartoon chef robot in a tall white hat in a cozy kitchen, carefully "
        "portioning small glowing token-shaped ingredients into measuring cups "
        "of different sizes. A recipe scroll on the wall shows tiny pictograms. "
        "A small fridge in the background labeled with a snowflake icon.",
        "16:9",
    ),
    (
        "part-10-idea-to-product/module-48-shipping-deploying/images/ch26-observability-dashboard.png",
        "A small mission-control room with three robot operators sitting at "
        "consoles facing a wall of glowing monitors. Each monitor shows a "
        "different small chart (a meter, a timeline, a heatmap). A bright red "
        "warning zone glows on one of the meters. Cool blue ambient lighting.",
        "16:9",
    ),
    (
        "part-10-idea-to-product/module-48-shipping-deploying/images/ch26-error-recovery-safety-net.png",
        "A circus-tent interior scene with a robot trapeze artist mid-flip high "
        "in the air. Three horizontal safety nets stretched at different heights "
        "below: top net, middle net, lower net. Each net has a different color. "
        "A spotlight illuminates the falling robot.",
        "16:9",
    ),
    (
        "part-12-frontiers/module-61-frontier-architectures/images/ch34-world-model-snowglobe.png",
        "A friendly robot holding up a glass snow globe containing a miniature "
        "simulated cartoon world inside (tiny buildings, tiny cars, tiny "
        "weather clouds). The robot tilts the globe and inspects it. Floating "
        "around the globe: small green checkmark icons and small red X icons.",
        "16:9",
    ),
    (
        "part-12-frontiers/module-61-frontier-architectures/images/ch34-opener-frontier-telescope.png",
        "A friendly robot scientist standing on a rocky mountain peak, looking "
        "through a large brass telescope at a starry night sky. Each star is a "
        "different small shape (gear, brain, atom, eye, key). A winding path "
        "trails down the mountain behind the robot showing the journey.",
        "16:9",
    ),
    (
        "part-12-frontiers/module-61-frontier-architectures/images/ch34-emergence-mirage.png",
        "Two-panel illustration split down the middle. Left panel: a desert "
        "scene where a robot finds a real shimmering oasis with palm trees at "
        "the top of a sand dune. Right panel: same desert scene but the oasis "
        "is fading into a smooth gradient mirage, and the robot wears small "
        "round measurement-glasses to see through it.",
        "16:9",
    ),
    (
        "part-12-frontiers/module-61-frontier-architectures/images/ch34-alternative-architectures-zoo.png",
        "A friendly cartoon zoo with four enclosures arranged in a row. First "
        "enclosure: a majestic eagle perched on a rock (transformer). Second: "
        "a sleek snake coiled (state space model). Third: a many-headed hydra "
        "(mixture of experts). Fourth: a wise owl with a book (retrieval). A "
        "small visitor robot reads a guidebook.",
        "16:9",
    ),
    (
        "part-12-frontiers/module-62-frontier-theory/images/ch34-system1-system2-thinking.png",
        "Two-panel illustration. Left panel: a robot sitting at a desk blurts "
        "out an answer with a lightning-bolt thought bubble, looks startled. "
        "Right panel: same robot at the same desk, but now carefully working "
        "through a chain of small interconnected thought-bubble boxes, looking "
        "calm and focused.",
        "16:9",
    ),
    (
        "part-12-frontiers/module-62-frontier-theory/images/ch34-memory-filing-cabinet.png",
        "A cross-section of a robot's head showing three memory compartments "
        "inside. Top: a small bright workspace with floating active items "
        "(working memory). Middle: a medium-sized filing cabinet with labeled "
        "drawers (episodic memory). Bottom: a vast library of books stretching "
        "into the distance (parametric memory). Warm cozy lighting.",
        "16:9",
    ),
    (
        "part-9-safety-security-ethics/module-38-agent-safety-security/images/ch24-castle-defense-v3.png",
        "A friendly cartoon medieval castle with three concentric defense "
        "layers: a wide blue moat with friendly fish, a tall stone outer wall, "
        "and an inner keep tower. A small robot king with a tiny crown sits "
        "safely inside the central keep. Pennants flutter from the towers. "
        "Sunny sky.",
        "16:9",
    ),
    (
        "part-9-safety-security-ethics/module-38-agent-safety-security/images/ch26-sandbox-fishbowl.png",
        "A small busy robot working inside a transparent round glass fishbowl "
        "sitting on a wooden desk. Inside the fishbowl: a tiny computer, "
        "tiny tools, tiny books. Outside the fishbowl: a much larger room "
        "labeled with a server-rack icon, kept safely separate.",
        "16:9",
    ),
    (
        "part-9-safety-security-ethics/module-38-agent-safety-security/images/ch26-supply-chain-security.png",
        "A robot inspector with a clipboard standing beside a conveyor belt. "
        "Packages roll along the belt through an X-ray scanner arch. Some "
        "packages glow soft green (safe), one package glows red and is being "
        "moved aside into a small quarantine bin with a warning symbol. Friendly "
        "factory setting.",
        "16:9",
    ),
]


def generate_one(job: tuple[str, str, str]) -> tuple[str, bool, str]:
    rel_path, subject, aspect = job
    out_path = ROOT / rel_path
    out_path.parent.mkdir(parents=True, exist_ok=True)
    prompt = f"{STYLE}\n\nSubject: {subject}"

    for attempt in range(3):
        try:
            response = CLIENT.models.generate_content(
                model=MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE"],
                    image_config=types.ImageConfig(
                        aspect_ratio=aspect,
                        image_size="1K",
                    ),
                ),
            )
            for part in response.parts:
                if part.inline_data:
                    img = part.as_image()
                    img.save(str(out_path))
                    return (rel_path, True, f"saved {out_path.stat().st_size} bytes")
            return (rel_path, False, "no image part in response")
        except Exception as e:
            if attempt < 2:
                time.sleep(5 * (2 ** attempt))
            else:
                return (rel_path, False, f"error: {e!r}")
    return (rel_path, False, "exhausted retries")


def main() -> int:
    print(f"Generating {len(JOBS)} images with {MODEL}", flush=True)
    successes = 0
    failures = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
        for rel_path, ok, msg in ex.map(generate_one, JOBS):
            status = "OK" if ok else "FAIL"
            print(f"[{status}] {rel_path}: {msg}", flush=True)
            if ok:
                successes += 1
            else:
                failures.append((rel_path, msg))
    print(f"\nDone: {successes}/{len(JOBS)} succeeded", flush=True)
    if failures:
        print("Failures:", flush=True)
        for rel_path, msg in failures:
            print(f"  {rel_path}: {msg}", flush=True)
    return 0 if successes == len(JOBS) else 1


if __name__ == "__main__":
    sys.exit(main())
