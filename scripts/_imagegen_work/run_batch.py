"""Submit all opener images as a single Gemini Batch API job (50% cost).

Reads targets.json produced by build_targets.py, builds InlinedRequest objects,
submits a batch, polls until done, then writes each returned PNG to the
correct part/chapter images/ directory.
"""
from __future__ import annotations

import base64
import json
import sys
import time
from pathlib import Path

WORK = Path(__file__).parent
TARGETS_FILE = WORK / "targets.json"
RESULTS_FILE = WORK / "results.json"
RAW_DIR = WORK / "raw"


def load_config() -> dict:
    p = Path.home() / ".gemini-imagegen.json"
    return json.loads(p.read_text())


def main() -> int:
    if not TARGETS_FILE.exists():
        print(f"Missing {TARGETS_FILE}; run build_targets.py first.")
        return 1
    targets = json.loads(TARGETS_FILE.read_text(encoding="utf-8"))
    if not targets:
        print("No targets.")
        return 0

    cfg = load_config()
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=cfg["api_key"])

    # Use Gemini image preview model for batch (compatible with batches.create).
    # Imagen 4 isn't supported via the batches.create() InlinedRequest path
    # documented in this SDK version; gemini-3-pro-image-preview gives the
    # 50% batch discount and produces 1K-quality cartoon illustrations.
    model = "gemini-3-pro-image-preview"

    inline_requests = []
    for t in targets:
        inline_requests.append(types.InlinedRequest(
            contents=[types.Content(parts=[types.Part(text=t["prompt"])], role="user")],
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"],
                image_config=types.ImageConfig(
                    aspect_ratio="16:9",
                    image_size="1K",
                ),
            ),
        ))

    print(f"Submitting batch of {len(inline_requests)} requests to {model}...")
    batch_job = client.batches.create(
        model=model,
        src=inline_requests,
        config={"display_name": f"llmbook-openers-{int(time.time())}"},
    )
    job_name = batch_job.name
    print(f"  Job: {job_name}")
    (WORK / "job.txt").write_text(job_name, encoding="utf-8")

    poll = 15
    last_state = None
    while True:
        batch_job = client.batches.get(name=job_name)
        state = batch_job.state.name if hasattr(batch_job.state, "name") else str(batch_job.state)
        if state != last_state:
            print(f"  State: {state}")
            last_state = state
        if state in ("JOB_STATE_SUCCEEDED", "JOB_STATE_FAILED", "JOB_STATE_CANCELLED"):
            break
        time.sleep(poll)

    if state != "JOB_STATE_SUCCEEDED":
        print(f"Batch ended in state {state}.")
        return 2

    print("Saving images...")
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    results = []
    inlined = batch_job.dest.inlined_responses
    if len(inlined) != len(targets):
        print(f"WARN: got {len(inlined)} responses for {len(targets)} targets")

    for i, (t, resp_wrapper) in enumerate(zip(targets, inlined)):
        response = resp_wrapper.response
        status = "ok"
        saved_path = None
        if not response or not getattr(response, "candidates", None):
            status = "no-candidates"
        else:
            saved = False
            for candidate in response.candidates:
                for part in candidate.content.parts:
                    if part.inline_data and part.inline_data.data:
                        img_data = part.inline_data.data
                        if isinstance(img_data, str):
                            img_data = base64.b64decode(img_data)
                        out_target = Path(t["output_path"])
                        out_target.parent.mkdir(parents=True, exist_ok=True)
                        out_target.write_bytes(img_data)
                        # also keep raw copy for size diagnostics
                        raw_copy = RAW_DIR / f"img_{i+1:03d}.png"
                        raw_copy.write_bytes(img_data)
                        saved_path = str(out_target)
                        saved = True
                        break
                if saved:
                    break
            if not saved:
                status = "no-inline-data"
        results.append({
            "idx": i,
            "kind": t["kind"],
            "part": t["part"],
            "module": t.get("module"),
            "h1": t["h1"],
            "output_path": t["output_path"],
            "alt": t["alt"],
            "status": status,
            "saved_path": saved_path,
        })

    RESULTS_FILE.write_text(json.dumps(results, indent=2), encoding="utf-8")
    n_ok = sum(1 for r in results if r["status"] == "ok")
    print(f"\nSaved {n_ok}/{len(results)} images.")
    print(f"Results: {RESULTS_FILE}")
    return 0 if n_ok == len(results) else 3


if __name__ == "__main__":
    sys.exit(main())
