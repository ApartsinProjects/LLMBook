"""Retry the 6 failed wave60 image generations with delays between calls."""
import json
import os
import sys
import time
from pathlib import Path

ROOT = Path(r"E:\Projects\BookBlogsHome\LLMBook")
AGENT_SCRIPTS = ROOT / "agents" / "book-skills" / "scripts"
sys.path.insert(0, str(AGENT_SCRIPTS))

from generate_icons_gemini import generate_image_imagen, load_api_key  # noqa: E402

TASKS_JSON = ROOT / "scripts" / "wave60_imagen_tasks.json"
RETRY_NAMES = {
    "ch27-4-toolbox-vs-swiss-army",
    "ch28-3-graduated-conveyor",
    "ch33-2-three-cuts-buffet",
    "ch36-2-library-vs-framework",
    "ch40-4-latency-budget-stopwatch",
    "ch44-5-five-drift-thermostats",
}

DELAY_SECONDS = 75
MODEL = "imagen-4.0-generate-001"
INITIAL_COOLDOWN = 90

tasks = json.loads(TASKS_JSON.read_text(encoding="utf-8"))
retry = [t for t in tasks if t["name"] in RETRY_NAMES]
print(f"Retrying {len(retry)} failed tasks with {DELAY_SECONDS}s between requests...")

api_key = load_api_key()

print(f"Initial cooldown {INITIAL_COOLDOWN}s to let the quota window reset...")
time.sleep(INITIAL_COOLDOWN)

results = []
for i, t in enumerate(retry):
    name = t["name"]
    out = Path(t["output"])
    if out.exists():
        print(f"  SKIP {name} (already exists)")
        results.append((name, str(out), out.stat().st_size, 0.0, None))
        continue
    if i > 0:
        print(f"  ...sleeping {DELAY_SECONDS}s...")
        time.sleep(DELAY_SECONDS)
    # Up to 3 attempts: initial + 2 backoffs (60s, 120s) on 429
    attempts = 0
    backoffs = [60, 120]
    success = False
    while attempts < 3 and not success:
        t0 = time.time()
        try:
            path, size = generate_image_imagen(
                api_key, MODEL, t["prompt"], t["output"], ctx=None,
                aspect_ratio=t.get("aspect_ratio", "1:1"),
            )
            dt = time.time() - t0
            print(f"  OK   {name}: {size:,} bytes ({dt:.1f}s) -> {path}")
            results.append((name, path, size, dt, None))
            success = True
        except Exception as e:
            dt = time.time() - t0
            msg = str(e)
            if "429" in msg and attempts < 2:
                wait = backoffs[attempts]
                print(f"  RETRY {name}: 429, waiting {wait}s before retry {attempts+2}/3")
                time.sleep(wait)
                attempts += 1
                continue
            print(f"  FAIL {name}: {msg}")
            results.append((name, str(out), 0, dt, msg))
            break

ok = sum(1 for r in results if r[4] is None)
fail = sum(1 for r in results if r[4] is not None)
print(f"\nRetry done: {ok} generated, {fail} failed")
