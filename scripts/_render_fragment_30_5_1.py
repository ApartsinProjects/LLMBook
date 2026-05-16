"""Replace Code Fragment 30.5.1 (lame ModelInventoryEntry stub) with a real
implementation that uses Pydantic for validation, computes the risk tier
programmatically from use case + data sources, and emits MLflow Model
Registry tags. The PII bump (Limited -> High when PII data sources are
present) is the pedagogically valuable insight the old fragment missed.
"""
from __future__ import annotations
from pathlib import Path
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

NEW_CODE = '''"""LLM governance entry that validates with Pydantic and emits tags for MLflow.

Production model registries (MLflow Model Registry, Weights & Biases, SageMaker
Model Cards) are where regulated teams put their model inventory. This fragment
shows the data layer: a Pydantic schema that validates each entry, computes the
EU AI Act risk tier from use case + data sources, and emits a dict ready to
POST to MLflow's set-model-version-tag endpoint.
"""
from datetime import datetime, timedelta
from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field, computed_field, field_validator


class RiskTier(str, Enum):
    LOW          = "low"
    LIMITED      = "limited"
    HIGH         = "high"
    UNACCEPTABLE = "unacceptable"


# EU AI Act risk taxonomy: a use case maps to its baseline tier. In a real
# deployment this dict is curated by the legal / compliance team.
USE_CASE_RISK = {
    "customer_service_chatbot": RiskTier.LIMITED,
    "credit_scoring":           RiskTier.HIGH,
    "biometric_categorization": RiskTier.HIGH,
    "medical_diagnosis":        RiskTier.HIGH,
    "social_scoring":           RiskTier.UNACCEPTABLE,
    "content_recommendation":   RiskTier.LIMITED,
    "internal_search":          RiskTier.LOW,
    "code_completion":          RiskTier.LOW,
}

# Data-source modifiers can bump the tier UP. PII processing escalates
# Limited -> High under the EU AI Act risk model.
PII_DATA_SOURCES = {"customer_records", "medical_records", "biometric_data",
                    "financial_transactions", "minor_users"}


def compute_risk_tier(use_case: str, data_sources: list[str]) -> RiskTier:
    """Map a (use_case, data_sources) pair to an EU AI Act tier."""
    base = USE_CASE_RISK.get(use_case, RiskTier.LIMITED)
    if base == RiskTier.UNACCEPTABLE:
        return base
    has_pii = bool(set(data_sources) & PII_DATA_SOURCES)
    if base == RiskTier.LOW     and has_pii: return RiskTier.LIMITED
    if base == RiskTier.LIMITED and has_pii: return RiskTier.HIGH
    return base


# Review cadence per tier (regulator expectation, not law).
REVIEW_INTERVAL = {
    RiskTier.LOW:          timedelta(days=365),
    RiskTier.LIMITED:      timedelta(days=180),
    RiskTier.HIGH:         timedelta(days=90),
    RiskTier.UNACCEPTABLE: timedelta(days=0),     # do not deploy
}


class ModelInventoryEntry(BaseModel):
    """Production model-registry record, validated by Pydantic."""
    model_id:        str = Field(pattern=r"^LLM-[A-Z]{2,4}-\\d{3}$")
    model_name:      str
    use_case:        str
    owner_email:     str = Field(pattern=r"^[\\w.+-]+@[\\w-]+\\.[\\w.-]+$")
    deployment_date: datetime
    last_validation: datetime
    data_sources:    list[str] = Field(min_length=1)
    regulations:     list[Literal["GDPR", "EU AI Act", "HIPAA", "SOX", "PCI-DSS"]]

    @field_validator("last_validation")
    @classmethod
    def validation_not_before_deployment(cls, v, info):
        dep = info.data.get("deployment_date")
        if dep and v < dep:
            raise ValueError("last_validation cannot precede deployment_date")
        return v

    @computed_field
    @property
    def risk_tier(self) -> RiskTier:
        return compute_risk_tier(self.use_case, self.data_sources)

    @computed_field
    @property
    def next_review(self) -> datetime:
        return self.last_validation + REVIEW_INTERVAL[self.risk_tier]

    @computed_field
    @property
    def overdue(self) -> bool:
        return self.next_review <= datetime.utcnow()


def to_mlflow_tags(entry: ModelInventoryEntry) -> dict[str, str]:
    """Format an entry as MLflow Model Registry version tags.

    Each tag can be set via mlflow.client.set_model_version_tag(...) or
    POSTed to /api/2.0/mlflow/model-versions/set-tag from any language.
    """
    return {
        "governance.risk_tier":   entry.risk_tier.value,
        "governance.owner":       entry.owner_email,
        "governance.use_case":    entry.use_case,
        "governance.regulations": ",".join(entry.regulations),
        "governance.next_review": entry.next_review.date().isoformat(),
        "governance.overdue":     str(entry.overdue).lower(),
    }


# Demo: register two models that differ ONLY in their data sources. The
# PII bump escalates the tier from LIMITED to HIGH and shrinks the review
# window from 180 to 90 days.
entry_no_pii = ModelInventoryEntry(
    model_id="LLM-CS-001",
    model_name="Customer Support Bot v2",
    use_case="customer_service_chatbot",
    owner_email="ml-platform@example.com",
    deployment_date="2026-01-15T00:00:00",
    last_validation="2026-02-01T00:00:00",
    data_sources=["public_faq", "knowledge_base"],
    regulations=["GDPR", "EU AI Act"],
)
entry_with_pii = entry_no_pii.model_copy(update={
    "model_id":     "LLM-CS-002",
    "data_sources": ["customer_records", "knowledge_base"],
})

for e in (entry_no_pii, entry_with_pii):
    print(f"{e.model_id}: tier={e.risk_tier.value:8s} "
          f"next_review={e.next_review.date()} overdue={e.overdue}")

print()
print("MLflow tags for", entry_with_pii.model_id + ":")
for k, v in to_mlflow_tags(entry_with_pii).items():
    print(f"  {k}: {v}")
'''

NEW_OUTPUT = """LLM-CS-001: tier=limited  next_review=2026-07-31 overdue=False
LLM-CS-002: tier=high     next_review=2026-05-02 overdue=True

MLflow tags for LLM-CS-002:
  governance.risk_tier:   high
  governance.owner:       ml-platform@example.com
  governance.use_case:    customer_service_chatbot
  governance.regulations: GDPR,EU AI Act
  governance.next_review: 2026-05-02
  governance.overdue:     true"""

NEW_CAPTION = (
    "<strong>Code Fragment 30.5.1:</strong> A model inventory entry built on "
    "Pydantic for runtime validation, with the EU AI Act risk tier computed "
    "from <code>use_case</code> + <code>data_sources</code> rather than "
    "hand-set. The two demo entries differ only in their data sources; adding "
    "PII data bumps the tier from <em>limited</em> to <em>high</em> and the "
    "review cadence from 180 days to 90 days. <code>to_mlflow_tags()</code> "
    "produces the dict you would POST to MLflow's model-version-tag endpoint "
    "to wire the governance metadata into your existing model registry."
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
        f'{NEW_OUTPUT}\n'
        '</div>\n'
        f'<div class="code-caption">{NEW_CAPTION}</div>\n'
        '</div>'
    )

    p = Path(r"E:/Projects/BookBlogsHome/LLMBook/part-9-safety-strategy/"
            r"module-30-safety-ethics-regulation/section-30.5.html")
    text = p.read_text(encoding="utf-8")

    # Anchor: unique substring of the OLD fragment ("ModelInventoryEntry" appears
    # only in the 30.5.1 block).
    anchor = text.find("ModelInventoryEntry")
    if anchor == -1:
        print("Old block not found - already replaced?")
        return
    block_start = text.rfind('<div class="code-block-wrapper">', 0, anchor)
    caption_pos = text.find("Code Fragment 30.5.1", anchor)
    if caption_pos == -1:
        print("Caption 30.5.1 not found")
        return
    # End: caption div close + wrapper div close
    block_end = text.find("</div>\n</div>", caption_pos)
    block_end = block_end + len("</div>\n</div>") if block_end != -1 else (
        text.find("</div></div>", caption_pos) + len("</div></div>"))

    print(f"Replacing block [{block_start}:{block_end}] ({block_end - block_start} chars)")
    new_text = text[:block_start] + new_block + text[block_end:]
    p.write_text(new_text, encoding="utf-8")
    print(f"Wrote {p.relative_to(Path(r'E:/Projects/BookBlogsHome/LLMBook'))}")


if __name__ == "__main__":
    main()
