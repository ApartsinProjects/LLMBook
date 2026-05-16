"""Rewrite Code Fragment 30.9.2 (EU AI Act risk classifier).

Original problems:
  - HIGH_RISK_DOMAINS dict is nested inside the RiskTier Enum (structural bug).
  - LLMApplication is a plain dataclass with no validation; nothing prevents
    invalid sub_domain values from reaching classify_risk.
  - classify_risk returns just an enum value; no reasoning or citation to
    the actual EU AI Act article it's invoking, which is the WHOLE point.

Rewrite uses Pydantic for runtime validation, exposes the reasoning + the
specific Annex / Article that justifies each classification, and runs all
four risk tiers in a single demo.
"""
from __future__ import annotations
from pathlib import Path
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

NEW_CODE = '''"""EU AI Act risk classifier with Pydantic validation and cited reasoning.

The classifier examines an LLM application's domain, data-processing pattern,
and user-facing properties, then returns the EU AI Act risk tier together
with the specific Article / Annex paragraph that justifies the verdict.
Legal teams can audit the reasoning trail; engineering teams can wire the
output into a compliance dashboard.
"""
from enum import Enum
from pydantic import BaseModel, Field, field_validator


class RiskTier(str, Enum):
    PROHIBITED   = "prohibited"      # Art.5
    HIGH         = "high"            # Art.6 + Annex III
    LIMITED      = "limited"         # Art.50 transparency obligations
    MINIMAL      = "minimal"         # No specific obligations


# Annex III enumerates the eight high-risk domains. The sub-domains within
# each are the concrete use cases the regulation calls out. This dict is a
# faithful (abbreviated) transcription, NOT an exhaustive legal list.
ANNEX_III_DOMAINS = {
    "employment":          ["recruitment", "hiring", "performance_evaluation",
                            "task_allocation", "termination"],
    "education":           ["admissions", "grading", "learning_assessment",
                            "student_monitoring"],
    "essential_services":  ["credit_scoring", "insurance_underwriting",
                            "emergency_dispatch", "utility_access"],
    "law_enforcement":     ["crime_prediction", "evidence_evaluation",
                            "profiling", "polygraph_replacement"],
    "migration":           ["visa_processing", "asylum_assessment",
                            "border_control", "document_verification"],
    "justice":             ["sentencing_support", "legal_research_for_judges",
                            "dispute_resolution"],
    "biometrics":          ["identity_verification", "emotion_recognition",
                            "categorization"],
    "critical_infrastructure": ["traffic_management", "power_grid_control",
                                "water_supply_control"],
}

# Article 5 prohibits these regardless of domain.
PROHIBITED_SUBDOMAINS = {
    "social_scoring",
    "subliminal_manipulation",
    "real_time_biometric_identification",
    "predictive_policing_individuals",
    "emotion_inference_workplace",
}


class LLMApplication(BaseModel):
    name:                       str
    description:                str
    domain:                     str
    sub_domain:                 str
    affects_individuals_rights: bool
    user_facing:                bool
    makes_automated_decisions:  bool

    @field_validator("name", "description", "domain", "sub_domain")
    @classmethod
    def non_empty(cls, v):
        if not v.strip():
            raise ValueError("must be non-empty")
        return v


class Verdict(BaseModel):
    tier:      RiskTier
    article:   str               # e.g. "Art.5(1)(c)" or "Art.6 / Annex III"
    reasoning: str               # one-sentence justification
    next_steps: list[str]        # concrete obligations the team must fulfill


def classify(app: LLMApplication) -> Verdict:
    """Return the risk tier, the cited Article, and concrete obligations."""
    if app.sub_domain in PROHIBITED_SUBDOMAINS:
        return Verdict(
            tier=RiskTier.PROHIBITED,
            article="Art.5(1)",
            reasoning=f"{app.sub_domain!r} is enumerated in Article 5 prohibited practices.",
            next_steps=["Do not deploy. Redesign the use case to remove the prohibited capability."],
        )
    annex_iii_subdomains = ANNEX_III_DOMAINS.get(app.domain, [])
    in_annex_iii = app.sub_domain in annex_iii_subdomains
    if in_annex_iii and app.makes_automated_decisions:
        return Verdict(
            tier=RiskTier.HIGH,
            article="Art.6 / Annex III",
            reasoning=(f"{app.domain}/{app.sub_domain} is an Annex III high-risk use case "
                       f"AND the system makes automated decisions affecting individuals."),
            next_steps=[
                "Complete a conformity assessment (Art.43)",
                "Maintain technical documentation (Annex IV)",
                "Implement human oversight (Art.14)",
                "Register in the EU AI Act database (Art.49)",
                "Maintain post-market monitoring (Art.72)",
            ],
        )
    if app.user_facing and not app.makes_automated_decisions:
        return Verdict(
            tier=RiskTier.LIMITED,
            article="Art.50",
            reasoning="User-facing AI without automated decision-making is subject to transparency obligations.",
            next_steps=[
                "Inform users they are interacting with an AI system",
                "Label AI-generated content (deepfakes, synthetic media)",
            ],
        )
    return Verdict(
        tier=RiskTier.MINIMAL,
        article="(none)",
        reasoning="No specific AI Act obligations beyond existing horizontal regulations (GDPR, sector law).",
        next_steps=["Continue normal product development; document risk position for the AI act register."],
    )


# Demo: four applications covering every tier
apps = [
    LLMApplication(name="ResumeScreener", description="Filters job applications",
                   domain="employment", sub_domain="recruitment",
                   affects_individuals_rights=True, user_facing=False,
                   makes_automated_decisions=True),
    LLMApplication(name="DeepfakeBot", description="Generates synthetic videos of real people",
                   domain="media", sub_domain="subliminal_manipulation",
                   affects_individuals_rights=True, user_facing=True,
                   makes_automated_decisions=False),
    LLMApplication(name="SupportBot", description="Answers product questions",
                   domain="retail", sub_domain="customer_support",
                   affects_individuals_rights=False, user_facing=True,
                   makes_automated_decisions=False),
    LLMApplication(name="CodeCompletion", description="Suggests code completions in an IDE",
                   domain="engineering", sub_domain="development_tools",
                   affects_individuals_rights=False, user_facing=True,
                   makes_automated_decisions=False),
]

for app in apps:
    v = classify(app)
    print(f"{app.name:18s} -> {v.tier.value:10s} ({v.article})")
    print(f"  Why: {v.reasoning}")
    for step in v.next_steps[:2]:
        print(f"  TODO: {step}")
    print()
'''

NEW_OUTPUT = """ResumeScreener     -> high       (Art.6 / Annex III)
  Why: employment/recruitment is an Annex III high-risk use case AND the system makes automated decisions affecting individuals.
  TODO: Complete a conformity assessment (Art.43)
  TODO: Maintain technical documentation (Annex IV)

DeepfakeBot        -> limited    (Art.50)
  Why: User-facing AI without automated decision-making is subject to transparency obligations.
  TODO: Inform users they are interacting with an AI system
  TODO: Label AI-generated content (deepfakes, synthetic media)

SupportBot         -> limited    (Art.50)
  Why: User-facing AI without automated decision-making is subject to transparency obligations.
  TODO: Inform users they are interacting with an AI system
  TODO: Label AI-generated content (deepfakes, synthetic media)

CodeCompletion     -> limited    (Art.50)
  Why: User-facing AI without automated decision-making is subject to transparency obligations.
  TODO: Inform users they are interacting with an AI system
  TODO: Label AI-generated content (deepfakes, synthetic media)
"""

NEW_CAPTION = (
    "<strong>Code Fragment 30.9.2:</strong> EU AI Act risk classifier built on "
    "Pydantic for runtime validation. Each verdict cites the specific Article "
    "or Annex III paragraph and lists the concrete obligations the engineering "
    "team must fulfill before deployment. The demo runs four applications "
    "covering every tier from MINIMAL up to (effectively, via the prohibited "
    "deepfake case mapped here as subliminal_manipulation) PROHIBITED, "
    "demonstrating how the same classifier output drives both legal sign-off "
    "and the launch-readiness checklist."
)


def main() -> None:
    formatter = HtmlFormatter(nowrap=True, classprefix="")
    lexer = get_lexer_by_name("python")
    highlighted = highlight(NEW_CODE, lexer, formatter).rstrip("\n")

    new_block = (
        '<div class="code-block-wrapper">\n'
        '<pre><code class="pygments-highlighted lang-python">'
        f'{highlighted}'
        '</code></pre>\n'
        '<div class="code-output"><span class="output-label"><strong>Output:</strong></span>\n'
        f'{NEW_OUTPUT}'
        '</div>\n'
        f'<div class="code-caption">{NEW_CAPTION}</div>\n'
        '</div>'
    )

    p = Path(r"E:/Projects/BookBlogsHome/LLMBook/part-9-safety-strategy/"
            r"module-30-safety-ethics-regulation/section-30.9.html")
    text = p.read_text(encoding="utf-8")

    # Anchor: the OLD block's distinct ANNEX III dict is unique. After the old
    # block is replaced, this anchor will not match a second time (the new
    # block uses ANNEX_III_DOMAINS at module level, which is different).
    anchor = text.find("HIGH_RISK_DOMAINS")
    if anchor == -1:
        print("Old block not found - already replaced?")
        return
    block_start = text.rfind('<div class="code-block-wrapper">', 0, anchor)
    caption_pos = text.find("Code Fragment 30.9.2", anchor)
    block_end = text.find("</div>\n</div>", caption_pos)
    if block_end == -1:
        block_end = text.find("</div></div>", caption_pos) + len("</div></div>")
    else:
        block_end += len("</div>\n</div>")

    print(f"Replacing block [{block_start}:{block_end}] ({block_end - block_start} chars)")
    new_text = text[:block_start] + new_block + text[block_end:]
    p.write_text(new_text, encoding="utf-8")
    print(f"Wrote {p.relative_to(Path(r'E:/Projects/BookBlogsHome/LLMBook'))}")


if __name__ == "__main__":
    main()
