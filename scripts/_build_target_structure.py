"""Build `book_structure.target.yaml` from `book_structure.yaml`.

Encodes the full restructuring plan as a series of transformations:

  1. Reorder parts: Frontiers (was X) -> XII, Idea-to-Product (was XI) -> X,
     Applications (was XII) -> XI.
  2. Rename parts: VII -> "Multimodal Generation",
     IX -> "Safety, Security & Ethics",
     X -> "Idea to Product",
     XI -> "Applications Across Industries".
  3. Dissolve Module 25 (Agent Safety, Production): 25.1/25.2/25.6/25.7 ->
     new Part IX Agent Safety chapter; 25.3/25.4 -> Part X Shipping; 25.5 ->
     Part VI Multi-Agent.
  4. Dissolve Module 27 (LLM Applications Across Industries): 27.1 -> Part X
     new Vibe-Coding chapter; 27.2 -> Part XI Finance; 27.3 -> Part XI
     Healthcare; 27.4 -> Part XI new Rec & Search chapter; 27.5 -> Part XI
     Cybersecurity; 27.6 -> split across Part XI Legal/Education + new
     Creative chapter; 27.7 -> Part VII new Embodied chapter.
  5. Dissolve Module 31 (Strategy/PM/ROI) into Part X.
  6. Expand Part X (Idea to Product) from 2 -> 10 chapters: Ideation, PM,
     Strategy, Vibe-Coding, MVP, Prototype-to-Prod, Compute, Scaling Econ,
     Shipping, Post-Launch.
  7. Expand Part XI (Applications) from 7 -> 9 chapters: add Creative
     Industries + Recommendation & Search.
  8. Expand Part VII (Multimodal) from 1 -> 2 chapters: split into
     Foundations + Embodied/World Models. Absorb old 33.4 from Frontiers.
  9. Expand Part XII (Frontiers) from 1 -> 4 chapters: Architectures,
     Theory, Systems & Hardware (NEW), AGI Trajectories (NEW).
  10. Add a "Tools of the Trade" closing chapter to every Part (12 new
      chapters total).
  11. Restructure appendices: drop G, H, I; regroup remaining 18 into
      4 themes (Foundations, Framework Guides, Infrastructure & MLOps,
      Pedagogical Kit).
  12. Full renumber chapters consecutively, 0 through N.

The output yaml is the TARGET state. The script _apply_migration.py
takes (current, target) and executes the moves.
"""
from __future__ import annotations
import argparse
import copy
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml not installed. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[1]


# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------

def find_part(struct: dict, slug: str) -> dict | None:
    for p in struct["parts"]:
        if p["slug"] == slug:
            return p
    return None


def find_chapter(struct: dict, slug: str) -> tuple[dict, dict] | None:
    """Find chapter by slug across all parts. Returns (part, chapter)."""
    for p in struct["parts"]:
        for c in p.get("chapters", []):
            if c["slug"] == slug:
                return (p, c)
    return None


def pop_chapter(struct: dict, slug: str) -> tuple[dict, dict] | None:
    """Find and remove a chapter from its part. Returns (old_part, chapter)."""
    res = find_chapter(struct, slug)
    if res is None:
        return None
    p, c = res
    p["chapters"].remove(c)
    return (p, c)


def section_lookup(chap: dict, num: str) -> dict | None:
    for s in chap.get("sections", []):
        if str(s["num"]) == str(num):
            return s
    return None


# ----------------------------------------------------------------------
# Transformations
# ----------------------------------------------------------------------

def t1_reorder_parts(t: dict) -> dict:
    """Frontiers -> Part XII; Idea-to-Product -> Part X; Applications -> XI."""
    swap = {
        "frontiers": (12, "XII"),
        "idea-to-product": (10, "X"),
        "llm-applications-across-industries": (11, "XI"),
    }
    for p in t["parts"]:
        if p["slug"] in swap:
            p["num"], p["roman"] = swap[p["slug"]]
    # Re-sort by num so the file is in canonical order
    t["parts"].sort(key=lambda p: p["num"])
    return t


def t2_rename_parts(t: dict) -> dict:
    """Apply the part-title rename per §7.5."""
    renames = {
        7: "Multimodal Generation",
        9: "Safety, Security & Ethics",
        10: "Idea to Product",
        11: "Applications Across Industries",
    }
    for p in t["parts"]:
        if p["num"] in renames:
            p["title"] = renames[p["num"]]
    # Also tweak slugs to match the new names for clarity
    slug_renames = {
        7: "multimodal-generation",
        9: "safety-security-ethics",
        10: "idea-to-product",
        11: "applications-across-industries",
    }
    for p in t["parts"]:
        if p["num"] in slug_renames:
            p["slug"] = slug_renames[p["num"]]
    return t


def t3_dissolve_module_25(t: dict) -> dict:
    """Module 25 (Agent Safety, Production & Operations) dissolves.

    25.1, 25.2, 25.6, 25.7 -> new Part IX Agent Safety chapter
    25.3, 25.4 -> Part X Shipping chapter (added in t6)
    25.5 -> Part VI Multi-Agent (chapter 23)
    """
    p, ch25 = pop_chapter(t, "agent-safety-production")
    secs = {s["num"]: s for s in ch25.get("sections", [])}

    # Move 25.5 -> Multi-Agent Systems chapter (23)
    multi_agent = find_chapter(t, "multi-agent-systems")
    if multi_agent and "25.5" in secs:
        s = secs.pop("25.5")
        # Renumber to 23.X (target chapter num filled later in renumber pass)
        s["num"] = "23.X"  # placeholder; finalized in t12
        s["_from"] = "25.5"
        multi_agent[1]["sections"].append(s)

    # New Agent Safety chapter in Part IX (after current Module 30)
    part_9 = next((p for p in t["parts"] if p["num"] == 9), None)
    new_agent_safety = {
        "num": None,  # finalized in t12
        "slug": "agent-safety-security",
        "title": "Agent Safety & Security",
        "subtitle": "Prompt-injection defense, sandboxing, supply-chain security, and agentic security benchmarks.",
        "sections": [
            {"num": "X.1", "slug": "section-x.1", "title": secs["25.1"]["title"], "_from": "25.1"},
            {"num": "X.2", "slug": "section-x.2", "title": secs["25.2"]["title"], "_from": "25.2"},
            {"num": "X.3", "slug": "section-x.3", "title": secs["25.6"]["title"], "_from": "25.6"},
            {"num": "X.4", "slug": "section-x.4", "title": secs["25.7"]["title"], "_from": "25.7"},
        ],
    }
    if part_9:
        part_9["chapters"].append(new_agent_safety)

    # 25.3 and 25.4 -> Part X (Idea to Product) Shipping chapter — staged in t6
    t["_staged_25_3_4"] = [secs.get("25.3"), secs.get("25.4")]
    return t


def t4_dissolve_module_27(t: dict) -> dict:
    """Module 27 (LLM Applications Across Industries) dissolves.

    27.1 -> Part X new Vibe-Coding chapter
    27.2 -> Part XI Finance (merged in)
    27.3 -> Part XI Healthcare (merged in)
    27.4 -> Part XI new Rec & Search chapter
    27.5 -> Part XI Cybersecurity (merged in)
    27.6 -> split: Legal/Education merge in; Creative -> new Part XI chapter
    27.7 -> Part VII new Embodied chapter
    """
    res = pop_chapter(t, "llm-applications")
    if not res:
        return t
    p, ch27 = res
    secs = {s["num"]: s for s in ch27.get("sections", [])}

    # Stage sections for the right new chapters (t6, t7, t8)
    t["_staged_27_1"] = secs.get("27.1")  # Vibe-Coding -> Part X
    t["_staged_27_4"] = secs.get("27.4")  # Rec & Search -> new Part XI chapter
    t["_staged_27_6"] = secs.get("27.6")  # Education+Legal+Creative split
    t["_staged_27_7"] = secs.get("27.7")  # Embodied -> Part VII

    # 27.2 Finance content merges into existing Part XI Finance chapter
    finance = find_chapter(t, "finance-llms")
    if finance and "27.2" in secs:
        s = secs["27.2"]
        s["_merge_into"] = "finance-llms"
        s["num"] = "XI.X"
        s["_from"] = "27.2"
        finance[1].setdefault("sections", []).append(s)

    # 27.3 Healthcare
    healthcare = find_chapter(t, "healthcare-llms")
    if healthcare and "27.3" in secs:
        s = secs["27.3"]
        s["_merge_into"] = "healthcare-llms"
        s["num"] = "XI.X"
        s["_from"] = "27.3"
        healthcare[1].setdefault("sections", []).append(s)

    # 27.5 Cybersecurity
    cyber = find_chapter(t, "cybersecurity-llms")
    if cyber and "27.5" in secs:
        s = secs["27.5"]
        s["_merge_into"] = "cybersecurity-llms"
        s["num"] = "XI.X"
        s["_from"] = "27.5"
        cyber[1].setdefault("sections", []).append(s)

    return t


def t5_dissolve_module_31(t: dict) -> dict:
    """Module 31 (Strategy, PM, ROI) dissolves into Part X chapters.

    31.1, 31.4 -> Strategy chapter (Part X)
    31.2 -> Product Management chapter (Part X)
    31.3, 31.7 -> Scaling Economics chapter (Part X)
    31.5, 31.6 -> Compute Planning chapter (Part X)
    """
    res = pop_chapter(t, "strategy-product-roi")
    if not res:
        return t
    p, ch31 = res
    secs = {s["num"]: s for s in ch31.get("sections", [])}
    t["_staged_31"] = secs
    return t


def t6_expand_idea_to_product(t: dict) -> dict:
    """Part X (Idea to Product) grows from 2 to 10 chapters."""
    p_x = next((p for p in t["parts"] if p["num"] == 10), None)
    if not p_x:
        return t

    # Existing 2 chapters: idea-to-product (34), shipping-scaling (35)
    # The 10-chapter cycle (Ideation -> Post-Launch). Author with placeholders;
    # _apply_migration will scaffold files for ones that don't exist on disk.
    secs_31 = t.get("_staged_31", {})
    sec_27_1 = t.get("_staged_27_1")
    staged_25_3_4 = t.get("_staged_25_3_4", [None, None])

    new_chapters = [
        {"slug": "ideation", "title": "Ideation: Finding LLM-Worthy Problems",
         "subtitle": "How to spot a problem the model actually solves.",
         "_new": True, "sections": [{"num": "X.1", "slug": "section-x.1",
                                       "title": "(authoring stub)", "_new": True}]},
        {"slug": "product-management", "title": "LLM Product Management",
         "subtitle": "Specs, evals, and the AI product manager's playbook.",
         "_new": True, "sections": _sec_from([secs_31.get("31.2")])},
        {"slug": "strategy-prioritization",
         "title": "LLM Strategy & Use Case Prioritization",
         "subtitle": "Build vs buy, vendor evaluation, value frontier.",
         "_new": True, "sections": _sec_from([secs_31.get("31.1"),
                                                  secs_31.get("31.4")])},
        {"slug": "vibe-coding",
         "title": "Prototyping via Vibe-Coding",
         "subtitle": "Building working software with LLM-assisted development.",
         "_new": True, "sections": _sec_from([sec_27_1])},
        {"slug": "mvp", "title": "Building the MVP",
         "subtitle": "What's the smallest thing that proves the hypothesis.",
         "_new": True, "sections": [{"num": "X.1", "slug": "section-x.1",
                                       "title": "(authoring stub)", "_new": True}]},
        # Existing: idea-to-product (was 34) becomes "From Prototype to Prod Hypothesis"
        # (renamed; reuses old file)
        # Compute, Scaling Econ, Shipping, Post-Launch:
        {"slug": "compute-planning",
         "title": "Compute Planning & Infrastructure",
         "subtitle": "Sizing infrastructure for the workload you'll actually run.",
         "_new": True, "sections": _sec_from([secs_31.get("31.5"),
                                                  secs_31.get("31.6")])},
        {"slug": "scaling-economics",
         "title": "Scaling Economics: Unit Costs & ROI",
         "subtitle": "What every LLM dollar buys, and when it stops scaling.",
         "_new": True, "sections": _sec_from([secs_31.get("31.3"),
                                                  secs_31.get("31.7")])},
        # shipping-scaling (was 35) becomes Shipping & Deploying, absorbs 25.3, 25.4
        {"slug": "post-launch-monitoring",
         "title": "Post-Launch Monitoring & Iteration",
         "subtitle": "Eval-in-prod, drift detection, retraining cadence.",
         "_new": True, "sections": [{"num": "X.1", "slug": "section-x.1",
                                       "title": "(authoring stub)", "_new": True}]},
    ]

    # Existing 34 -> "From Prototype to Production Hypothesis"
    existing_34 = next((c for c in p_x["chapters"]
                          if c["slug"] == "idea-to-product"), None)
    if existing_34:
        existing_34["title"] = "From Prototype to Production Hypothesis"
        existing_34["slug"] = "prototype-to-production"

    # Existing 35 -> "Shipping & Deploying" with 25.3/25.4 absorbed
    existing_35 = next((c for c in p_x["chapters"]
                          if c["slug"] == "shipping-scaling"), None)
    if existing_35:
        existing_35["title"] = "Shipping & Deploying AI Products"
        existing_35["slug"] = "shipping-deploying"
        for s in staged_25_3_4:
            if s is not None:
                existing_35["sections"].append({
                    **s, "num": "X.X", "_from": s.get("num"),
                })

    # Order: Ideation, PM, Strategy, Vibe-Coding, MVP, Prototype-to-Prod (old 34),
    # Compute, Scaling Econ, Shipping (old 35), Post-Launch.
    p_x["chapters"] = (
        new_chapters[0:5]  # Ideation, PM, Strategy, Vibe-Coding, MVP
        + ([existing_34] if existing_34 else [])
        + new_chapters[5:7]  # Compute, Scaling Econ
        + ([existing_35] if existing_35 else [])
        + new_chapters[7:]  # Post-Launch
    )
    return t


def _sec_from(sources):
    """Turn a list of (possibly None) source-section dicts into target sections."""
    out = []
    for i, s in enumerate(sources, 1):
        if s is None:
            continue
        out.append({
            "num": f"X.{i}",
            "slug": f"section-x.{i}",
            "title": s["title"],
            "_from": s["num"],
        })
    return out


def t7_expand_applications(t: dict) -> dict:
    """Part XI (Applications) grows from 7 to 9 chapters: add Creative + Rec&Search."""
    p_xi = next((p for p in t["parts"] if p["num"] == 11), None)
    if not p_xi:
        return t
    sec_27_4 = t.get("_staged_27_4")
    sec_27_6 = t.get("_staged_27_6")
    new_chapters = [
        {"slug": "creative-industries",
         "title": "LLMs in Creative Industries",
         "subtitle": "Music, video, design, marketing copy: the multimodal generation playbook for creative work.",
         "_new": True,
         "sections": _sec_from([sec_27_6]) if sec_27_6 else []},
        {"slug": "recommendation-search",
         "title": "LLM-Powered Recommendation & Search",
         "subtitle": "Ranking, retrieval, and personalization at scale.",
         "_new": True,
         "sections": _sec_from([sec_27_4]) if sec_27_4 else []},
    ]
    p_xi["chapters"].extend(new_chapters)
    return t


def t8_expand_multimodal(t: dict) -> dict:
    """Part VII (Multimodal Generation): split Module 26 into 2 chapters.

    Module 26 keeps 26.1-26.4 + new Streaming section.
    New Module 26 (Embodied): 26.5, 26.6, 26.7 + absorbed 33.4 + new sections.
    """
    p_vii = next((p for p in t["parts"] if p["num"] == 7), None)
    if not p_vii:
        return t

    mm = next((c for c in p_vii["chapters"] if c["slug"] == "multimodal"), None)
    if mm:
        # Trim mm to 26.1-26.4 + new Streaming
        mm["title"] = "Multimodal Generation Foundations"
        old_secs = {s["num"]: s for s in mm.get("sections", [])}
        mm["sections"] = []
        for n in ["26.1", "26.2", "26.3", "26.4"]:
            if n in old_secs:
                mm["sections"].append(old_secs[n])
        mm["sections"].append({
            "num": "X.5", "slug": "section-x.5",
            "title": "Streaming & Real-Time Multimodal",
            "_new": True,
        })

        # New chapter for embodied / world / reasoning
        sec_27_7 = t.get("_staged_27_7")
        embodied = {
            "slug": "embodied-world-models",
            "title": "Embodied AI, World Models & Multimodal Reasoning",
            "subtitle": "VLA models, robotics, world simulators, and cross-modal reasoning.",
            "_new": True,
            "sections": [
                # Move 26.5, 26.6, 26.7 here
                old_secs.get("26.5"),
                old_secs.get("26.6"),
                old_secs.get("26.7"),
            ],
        }
        # Add 33.4 (World Models) — staged later in t9 from Frontiers split
        embodied["sections"] = [s for s in embodied["sections"] if s]
        embodied["sections"].append({
            "num": "X.4", "slug": "section-x.4",
            "title": "World Models for Video Understanding (from old 33.4)",
            "_from": "33.4", "_new": True,
        })
        embodied["sections"].append({
            "num": "X.5", "slug": "section-x.5",
            "title": "3D Asset Generation & Neural Scenes",
            "_new": True,
        })
        embodied["sections"].append({
            "num": "X.6", "slug": "section-x.6",
            "title": "Multimodal Editing & Inpainting",
            "_new": True,
        })
        embodied["sections"].append({
            "num": "X.7", "slug": "section-x.7",
            "title": "Multimodal Reasoning & Cross-Modal Retrieval",
            "_new": True,
        })
        if sec_27_7:
            embodied["sections"].append({
                "num": "X.8", "slug": "section-x.8",
                "title": sec_27_7["title"],
                "_from": "27.7",
            })
        p_vii["chapters"].append(embodied)
    return t


def t9_expand_frontiers(t: dict) -> dict:
    """Part XII (Frontiers): expand from 1 to 4 chapters per the scout."""
    p_xii = next((p for p in t["parts"] if p["num"] == 12), None)
    if not p_xii:
        return t
    mod33 = next((c for c in p_xii["chapters"]
                   if c["slug"] == "emerging-architectures"), None)
    if not mod33:
        return t
    old_secs = {s["num"]: s for s in mod33.get("sections", [])}

    # Chapter 1: Frontier Architectures & Scaling (33.1, 33.2, 33.3, 33.10)
    arch = {
        "slug": "frontier-architectures",
        "title": "Frontier Architectures & Scaling",
        "subtitle": "Post-transformer architectures, extreme quantization, and what comes after Chinchilla.",
        "sections": [old_secs.get("33.1"), old_secs.get("33.2"),
                      old_secs.get("33.3"), old_secs.get("33.10")],
    }
    # Chapter 2: Frontier Theory & Cognition (33.5, 33.6, 33.7, 33.8)
    theory = {
        "slug": "frontier-theory",
        "title": "Frontier Theory & Cognition",
        "subtitle": "Formal theories of reasoning, memory primitives, mechanistic interpretability at scale.",
        "sections": [old_secs.get("33.5"), old_secs.get("33.6"),
                      old_secs.get("33.7"), old_secs.get("33.8")],
    }
    # Chapter 3: Frontier Systems & Hardware (NEW)
    systems = {
        "slug": "frontier-systems-hardware",
        "title": "Frontier Systems & Hardware",
        "subtitle": "Non-NVIDIA silicon, decentralized training, edge LLMs, training-inference co-design.",
        "_new": True,
        "sections": [
            {"num": "X.1", "slug": "section-x.1",
             "title": "Beyond NVIDIA: Groq, Cerebras, Tenstorrent, AMD MI355",
             "_new": True},
            {"num": "X.2", "slug": "section-x.2",
             "title": "Decentralized Training: Nous Psyche, DeMo, DisTrO",
             "_new": True},
            {"num": "X.3", "slug": "section-x.3",
             "title": "Edge LLMs: MLX, Apple Intelligence, Llama-Mobile",
             "_new": True},
            {"num": "X.4", "slug": "section-x.4",
             "title": "FlashAttention-4 and Inference Kernels for Blackwell",
             "_new": True},
            {"num": "X.5", "slug": "section-x.5",
             "title": "Training-Inference Co-Design",
             "_new": True},
        ],
    }
    # Chapter 4: AGI Trajectories & Open Questions (NEW + 33.11)
    agi = {
        "slug": "agi-trajectories",
        "title": "AGI Trajectories & Open Questions",
        "subtitle": "Frontier benchmarks, timeline debate, alignment-at-frontier, economic implications.",
        "_new": True,
        "sections": [
            {"num": "X.1", "slug": "section-x.1",
             "title": "Frontier Benchmarks: HLE, ARC-AGI-2, FrontierMath",
             "_new": True},
            {"num": "X.2", "slug": "section-x.2",
             "title": "Alignment at Frontier Scale",
             "_new": True},
            {"num": "X.3", "slug": "section-x.3",
             "title": "AGI Timelines: The 2027-2033 Spectrum",
             "_new": True},
            {"num": "X.4", "slug": "section-x.4",
             "title": "Economic Implications & Labor-Market Data",
             "_new": True},
            old_secs.get("33.11"),  # What 2026 Settled
        ],
    }

    # Filter Nones
    for c in (arch, theory, systems, agi):
        c["sections"] = [s for s in c["sections"] if s is not None]

    p_xii["chapters"] = [arch, theory, systems, agi]
    return t


def t10_add_tools_of_the_trade(t: dict) -> dict:
    """Add a closing 'Tools of the Trade' chapter to every Part."""
    suffixes = {
        1: "Foundations Stack",
        2: "Models & Tokenizers",
        3: "LLM API Stack",
        4: "Training & Adaptation Stack",
        5: "Retrieval & Conversation Stack",
        6: "Agent Stack",
        7: "Multimodal Stack",
        8: "Eval & Production Stack",
        9: "Safety & Guardrails Stack",
        10: "Idea-to-Product Toolkit",
        11: "Industry Solution Stack",
        12: "Frontier Research Stack",
    }
    for p in t["parts"]:
        suffix = suffixes.get(p["num"], "Toolkit")
        p["chapters"].append({
            "slug": "tools-of-the-trade",
            "title": f"Tools of the Trade: {suffix}",
            "subtitle": "Consolidated reference: platforms, libraries, datasets, models, and external resources for this part.",
            "_new": True,
            "sections": [
                {"num": "X.1", "slug": "section-x.1",
                 "title": "Platforms", "_new": True},
                {"num": "X.2", "slug": "section-x.2",
                 "title": "Libraries & Frameworks", "_new": True},
                {"num": "X.3", "slug": "section-x.3",
                 "title": "Datasets & Benchmarks", "_new": True},
                {"num": "X.4", "slug": "section-x.4",
                 "title": "Models", "_new": True},
                {"num": "X.5", "slug": "section-x.5",
                 "title": "External Reading & Communities", "_new": True},
            ],
        })
    return t


def t11_restructure_appendices(t: dict) -> dict:
    """Drop G, H, I. Regroup remaining 18 into 4 themes + Glossary."""
    keep_letters = set("ABCDEFJKLMNOPQRSTU")  # drop G, H, I
    new_apps = []
    for a in t["appendices"]:
        if a["letter"] in keep_letters:
            new_apps.append(a)
    # Assign group field
    group_map = {
        "A": "Foundations", "B": "Foundations", "C": "Foundations",
        "D": "Foundations", "E": "Foundations",
        "J": "Framework Guides", "K": "Framework Guides",
        "P": "Framework Guides",
        "F": "Infrastructure & MLOps", "L": "Infrastructure & MLOps",
        "M": "Infrastructure & MLOps", "N": "Infrastructure & MLOps",
        "O": "Infrastructure & MLOps", "Q": "Infrastructure & MLOps",
        "R": "Infrastructure & MLOps",
        "S": "Pedagogical Kit", "T": "Pedagogical Kit",
        "U": "Pedagogical Kit",
    }
    # Relabel letters consecutively in group order
    order = ["Foundations", "Framework Guides",
             "Infrastructure & MLOps", "Pedagogical Kit"]
    group_to_apps: dict[str, list[dict]] = {g: [] for g in order}
    for a in new_apps:
        g = group_map.get(a["letter"], "Other")
        a["group"] = g
        group_to_apps.setdefault(g, []).append(a)

    final = []
    next_letter = ord("A")
    for g in order:
        for a in group_to_apps.get(g, []):
            a["old_letter"] = a["letter"]
            a["letter"] = chr(next_letter)
            next_letter += 1
            final.append(a)
    t["appendices"] = final
    return t


def t12_renumber_chapters(t: dict) -> dict:
    """Full renumber: chapters flow 0..N consecutively across all parts."""
    n = 0
    for p in t["parts"]:
        for c in p.get("chapters", []):
            c["old_num"] = c.get("num")
            c["num"] = n
            n += 1
            # Renumber sections within chapter as N.1, N.2, ...
            for i, s in enumerate(c.get("sections", []), 1):
                s["old_num"] = s.get("num")
                s["num"] = f"{c['num']}.{i}"
                s["slug"] = f"section-{c['num']}.{i}"
    # Strip staged-data fields
    for k in list(t.keys()):
        if k.startswith("_staged"):
            del t[k]
    return t


# ----------------------------------------------------------------------
# Pipeline
# ----------------------------------------------------------------------

def transform(current: dict) -> dict:
    t = copy.deepcopy(current)
    t = t1_reorder_parts(t)
    t = t2_rename_parts(t)
    t = t3_dissolve_module_25(t)
    t = t4_dissolve_module_27(t)
    t = t5_dissolve_module_31(t)
    t = t6_expand_idea_to_product(t)
    t = t7_expand_applications(t)
    t = t8_expand_multimodal(t)
    t = t9_expand_frontiers(t)
    t = t10_add_tools_of_the_trade(t)
    t = t11_restructure_appendices(t)
    t = t12_renumber_chapters(t)
    return t


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--current", type=Path,
                    default=ROOT / "book_structure.yaml")
    ap.add_argument("--target", type=Path,
                    default=ROOT / "book_structure.target.yaml")
    args = ap.parse_args()

    current = yaml.safe_load(args.current.read_text(encoding="utf-8"))
    target = transform(current)
    args.target.write_text(
        yaml.dump(target, default_flow_style=False, sort_keys=False,
                   allow_unicode=True, width=200),
        encoding="utf-8",
    )

    # Summary
    n_parts = len(target["parts"])
    n_chaps = sum(len(p.get("chapters", [])) for p in target["parts"])
    n_secs = sum(len(c.get("sections", []))
                  for p in target["parts"] for c in p.get("chapters", []))
    n_apps = len(target["appendices"])
    print(f"Target structure:")
    print(f"  Parts: {n_parts}")
    print(f"  Chapters: {n_chaps}")
    print(f"  Sections: {n_secs}")
    print(f"  Appendices: {n_apps}")
    print(f"Wrote {args.target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
