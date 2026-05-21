"""Build the image-pass manifest (8 top-tier curated candidates) for run_comicgen.py."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent
OUT = ROOT / ".book-update" / "image-pass-manifest.jsonl"

C = [
 ("part-12-llm-systems-at-scale/module-59-distributed-training-systems/section-59.4.html",
  "images/pipeline-bubble-assembly-line.jpg", "MENTAL-MAP", "59.4",
  "A factory assembly line of four robot workers labeled GPU 1, GPU 2, GPU 3 and GPU 4 "
  "passing a product down a conveyor belt, each robot adding to a different micro-batch part. "
  "At the start and the end of the line some robots stand idle inside a grey shaded zone "
  "labeled 'the bubble (idle time)'. A small clock icon shows wasted time. Clear and instructive."),
 ("part-5-multimodal-llms/module-22-vision-language-models/section-22.2.html",
  "images/clip-shared-embedding-sky.jpg", "MENTAL-MAP", "22.2",
  "A wide open sky labeled 'shared embedding space'. A matching pair, an image balloon and its "
  "caption balloon, drift together and link with a short rope; mismatched image and caption "
  "balloons are pushed apart by little springs. One new image balloon labeled 'unseen image' "
  "floats toward the nearest text label, illustrating zero-shot transfer (CLIP contrastive learning)."),
 ("part-10-llm-security-runtime-safety/module-50-privacy-data-protection/section-50.1.html",
  "images/differential-privacy-fog.jpg", "MENTAL-MAP", "50.1",
  "A friendly crowd group-photo where one individual is gently hidden inside a soft cloud of "
  "small scattered dots labeled 'noise'. The overall crowd scene stays clearly readable (the "
  "aggregate), but that one person cannot be identified. A banner reads 'differential privacy: "
  "useful in aggregate, private per person'."),
 ("part-2-understanding-llms/module-10-interpretability/section-10.4.html",
  "images/attribution-detective-lenses.jpg", "MENTAL-MAP", "10.4",
  "A friendly cartoon detective re-tracing a language model's decision backward across a sentence, "
  "holding four differently colored magnifying lenses labeled 'attention rollout', 'gradients', "
  "'LRP' and 'perturbation'. Each lens highlights a slightly different set of words, showing that "
  "attribution methods can disagree about which words mattered."),
 ("part-12-llm-systems-at-scale/module-58-frontier-systems-hardware/section-58.5.html",
  "images/training-inference-codesign.jpg", "COMIC", "58.5",
  "A two-panel cartoon: an architect at a drafting table designs a building labeled 'the model' "
  "while two contractors argue over the same blueprint, one labeled 'Training' wanting a giant "
  "crane, the other labeled 'Inference' wanting a lean fast design; in the final panel they shake "
  "hands over a blueprint stamped 'co-design'."),
 ("part-10-llm-security-runtime-safety/module-48-guardrails-runtime-safety/section-48.1.html",
  "images/guardrails-bowling-bumpers.jpg", "MENTAL-MAP", "48.1",
  "A bowling lane with raised bumpers labeled 'guardrails' on both sides. A ball labeled "
  "'model output' rolls toward pins labeled 'user'; a wild throw is safely deflected by a bumper. "
  "A small sign clarifies 'guardrails catch unsafe outputs at runtime; they are not the model's "
  "alignment'."),
 ("part-7-retrieval-information-extraction-with-llms/module-33-cross-modal-reasoning-rag/section-33.3.html",
  "images/retrieve-vs-reason-switchboard.jpg", "MENTAL-MAP", "33.3",
  "A vintage telephone switchboard operator labeled 'router' connecting each incoming question to "
  "one of four pneumatic tubes labeled 'answer from memory', 'retrieve and look it up', "
  "'reason step by step' and 'use a tool', illustrating the retrieve-versus-reason routing policy."),
 ("part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.5.html",
  "images/adam-vs-sgd-hikers.jpg", "COMIC", "6.5",
  "A cartoon of two hikers descending a foggy ravine toward a small flag labeled 'minimum'. One "
  "hiker labeled 'SGD' bounces wildly off both canyon walls with one fixed stride length. The "
  "other labeled 'Adam' wears smart boots that take short careful steps on steep narrow stretches "
  "and longer steps on flat stretches (adaptive per-parameter step size), descending smoothly."),
]

with OUT.open("w", encoding="utf-8") as f:
    for i, (sec, fn, kind, cs, prompt) in enumerate(C, 1):
        f.write(json.dumps({
            "section": str(ROOT / sec), "filename": fn, "kind": kind,
            "chap_sec": cs, "num": i, "section_exists": (ROOT / sec).exists(),
            "prompt": prompt}) + "\n")
print("wrote", OUT, "rows:", len(C), "all sections exist:",
      all((ROOT / s[0]).exists() for s in C))
