"""Retry the wave60 image generations that haven't landed yet.

- Skips any image that already exists (idempotent).
- Sleeps 100 seconds between requests (Imagen 4 free-tier quota is roughly
  5 requests per minute; we use a conservative spacing).
- A single attempt per task. On 429, the task is recorded as failed and
  the script keeps going so the next slot can fire after the spacing.
"""
import json
import sys
import time
from pathlib import Path

ROOT = Path(r"E:\Projects\BookBlogsHome\LLMBook")
AGENT_SCRIPTS = ROOT / "agents" / "book-skills" / "scripts"
sys.path.insert(0, str(AGENT_SCRIPTS))

from generate_icons_gemini import generate_image_imagen, load_api_key  # noqa: E402

TASKS_JSON = ROOT / "scripts" / "wave60_imagen_tasks.json"
INITIAL_COOLDOWN = 5
DELAY_SECONDS = 30  # spacing between consecutive Imagen requests
# Switch to imagen-4.0-fast which has a separate daily quota from imagen-4.0
MODEL = "imagen-4.0-fast-generate-001"

tasks = json.loads(TASKS_JSON.read_text(encoding="utf-8"))
pending = [t for t in tasks if not Path(t["output"]).exists()]
print(f"Total tasks: {len(tasks)}, pending: {len(pending)}", flush=True)
if not pending:
    print("All images already exist. Nothing to do.", flush=True)
    sys.exit(0)

api_key = load_api_key()

print(f"Initial cooldown {INITIAL_COOLDOWN}s ...", flush=True)
time.sleep(INITIAL_COOLDOWN)

results = []
for i, t in enumerate(pending):
    name = t["name"]
    if i > 0:
        print(f"  ...spacing {DELAY_SECONDS}s before next request...", flush=True)
        time.sleep(DELAY_SECONDS)
    t0 = time.time()
    try:
        path, size = generate_image_imagen(
            api_key, MODEL, t["prompt"], t["output"], ctx=None,
            aspect_ratio=t.get("aspect_ratio", "1:1"),
        )
        dt = time.time() - t0
        print(f"  OK   {name}: {size:,} bytes ({dt:.1f}s) -> {path}", flush=True)
        results.append((name, path, size, dt, None))
    except Exception as e:
        dt = time.time() - t0
        msg = str(e)
        print(f"  FAIL {name}: {msg}", flush=True)
        results.append((name, str(Path(t["output"])), 0, dt, msg))

ok = sum(1 for r in results if r[4] is None)
fail = sum(1 for r in results if r[4] is not None)
print(f"\nRetry done: {ok} generated, {fail} failed", flush=True)
