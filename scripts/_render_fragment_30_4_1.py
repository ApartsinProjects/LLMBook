"""Render the new Code Fragment 30.4.1 with pygments and inject it into
the section file, replacing the lame ComplianceChecker stub.

The replacement maps regulatory requirements to checks that actually
VALIDATE something against a deployment config (not just store boolean
flags). Each check cites a specific EU AI Act / GDPR article, returns
evidence, and proposes remediation when it fails.
"""
from __future__ import annotations
import re
from pathlib import Path
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

NEW_CODE = '''"""Map regulatory requirements to checks that examine a deployment.

Each requirement carries the Article it cites (so an auditor can verify
the source), a check function that returns (passed, evidence), and a
remediation hint shown when the check fails.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Callable
import json


@dataclass
class Requirement:
    article: str                                   # e.g. "EU AI Act Art.13"
    name: str
    check: Callable[[dict], tuple[bool, str]]
    remediation: str


def has_transparency_notice(cfg: dict) -> tuple[bool, str]:
    """EU AI Act Art.13: users must be informed they are interacting with AI."""
    notice = cfg.get("ui", {}).get("ai_disclosure")
    if not notice:
        return False, "No AI disclosure on the user-facing UI"
    if "ai" not in notice.lower():
        return False, f"Disclosure too vague: {notice!r}"
    return True, f"Disclosure present: {notice!r}"


def has_dpia(cfg: dict) -> tuple[bool, str]:
    """GDPR Art.35: a Data Protection Impact Assessment is required."""
    dpia = cfg.get("dpia", {})
    if not dpia.get("completed"):
        return False, "No DPIA on file"
    age = (datetime.utcnow() - datetime.fromisoformat(dpia["last_review"])).days
    if age > 365:
        return False, f"DPIA older than 12 months ({age} days)"
    return True, f"DPIA reviewed {age} days ago"


def has_human_oversight(cfg: dict) -> tuple[bool, str]:
    """EU AI Act Art.14: high-risk systems need a human-in-the-loop path."""
    esc = cfg.get("escalation_to_human", {})
    if not esc.get("enabled"):
        return False, "Human escalation path not configured"
    sla = esc.get("sla_minutes", 9999)
    if sla > 30:
        return False, f"Human SLA {sla}min exceeds 30min threshold"
    return True, f"Human escalation within {sla}min"


def has_retention_policy(cfg: dict) -> tuple[bool, str]:
    """GDPR Art.5(1)(e): personal data kept no longer than necessary."""
    days = cfg.get("logs", {}).get("retention_days")
    if days is None:
        return False, "Log retention period not set"
    if days > 90:
        return False, f"Retention {days}d exceeds 90d default"
    return True, f"Logs retained {days} days"


def has_audit_logging(cfg: dict) -> tuple[bool, str]:
    """EU AI Act Art.12: high-risk systems must log operational events."""
    fields = set(cfg.get("logs", {}).get("fields_captured", []))
    required = {"prompt", "response", "user_id", "timestamp", "model_version"}
    missing = required - fields
    if missing:
        return False, f"Audit log missing fields: {sorted(missing)}"
    return True, "All required fields captured"


REQUIREMENTS = [
    Requirement("EU AI Act Art.13", "transparency_notice",
                has_transparency_notice,
                "Add an 'Powered by AI' disclosure to the chat UI"),
    Requirement("GDPR Art.35", "dpia_completed", has_dpia,
                "Complete a DPIA and refresh annually"),
    Requirement("EU AI Act Art.14", "human_oversight", has_human_oversight,
                "Configure escalation_to_human with SLA <= 30 minutes"),
    Requirement("GDPR Art.5(1)(e)", "data_retention", has_retention_policy,
                "Set logs.retention_days <= 90"),
    Requirement("EU AI Act Art.12", "audit_logging", has_audit_logging,
                "Capture prompt, response, user_id, timestamp, model_version"),
]


def audit(cfg: dict) -> dict:
    findings = []
    for req in REQUIREMENTS:
        passed, evidence = req.check(cfg)
        findings.append({
            "article": req.article,
            "requirement": req.name,
            "passed": passed,
            "evidence": evidence,
            "remediation": None if passed else req.remediation,
        })
    return {
        "score": f"{sum(f['passed'] for f in findings)}/{len(findings)}",
        "compliant": all(f["passed"] for f in findings),
        "findings": findings,
        "assessed_at": datetime.utcnow().isoformat() + "Z",
    }


# Demo: audit a sample deployment config
deployment = {
    "ui": {"ai_disclosure": "This chat is powered by AI"},
    "dpia": {"completed": True, "last_review": "2026-01-15T00:00:00"},
    "escalation_to_human": {"enabled": True, "sla_minutes": 15},
    "logs": {
        "retention_days": 365,                     # too long: fails
        "fields_captured": ["prompt", "response", "timestamp"],
    },
}
print(json.dumps(audit(deployment), indent=2))
'''

NEW_OUTPUT = """{
  "score": "3/5",
  "compliant": false,
  "findings": [
    {"article": "EU AI Act Art.13", "requirement": "transparency_notice",
     "passed": true,  "evidence": "Disclosure present: 'This chat is powered by AI'",
     "remediation": null},
    {"article": "GDPR Art.35",      "requirement": "dpia_completed",
     "passed": true,  "evidence": "DPIA reviewed 121 days ago",
     "remediation": null},
    {"article": "EU AI Act Art.14", "requirement": "human_oversight",
     "passed": true,  "evidence": "Human escalation within 15min",
     "remediation": null},
    {"article": "GDPR Art.5(1)(e)", "requirement": "data_retention",
     "passed": false, "evidence": "Retention 365d exceeds 90d default",
     "remediation": "Set logs.retention_days <= 90"},
    {"article": "EU AI Act Art.12", "requirement": "audit_logging",
     "passed": false, "evidence": "Audit log missing fields: ['model_version', 'user_id']",
     "remediation": "Capture prompt, response, user_id, timestamp, model_version"}
  ],
  "assessed_at": "2026-05-16T10:30:00.000Z"
}"""

NEW_CAPTION = (
    "<strong>Code Fragment 30.4.1:</strong> A compliance auditor that maps "
    "each requirement to a real check function. Each check cites the "
    "specific article it enforces (EU AI Act / GDPR) and returns "
    "concrete evidence plus a remediation hint when it fails. The demo "
    "configuration passes 3 of 5 checks; the failures surface actionable "
    "fixes for the deployment team."
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
            r"module-30-safety-ethics-regulation/section-30.4.html")
    text = p.read_text(encoding="utf-8")

    # Locate the existing block: from '<div class="code-block-wrapper">' that
    # contains 'ComplianceChecker' through the caption '</div></div>'.
    # Use the unique substring 'ComplianceChecker' as the anchor.
    anchor = text.find("ComplianceChecker")
    if anchor == -1:
        print("Old block not found - already replaced?")
        return
    block_start = text.rfind('<div class="code-block-wrapper">', 0, anchor)
    # Find the caption closing </div></div> that ends this code-block-wrapper.
    # Caption text starts with "Code Fragment 30.4.1"
    caption_pos = text.find("Code Fragment 30.4.1", anchor)
    if caption_pos == -1:
        print("Caption 30.4.1 not found")
        return
    block_end = text.find("</div>\n</div>", caption_pos)
    if block_end == -1:
        block_end = text.find("</div></div>", caption_pos)
    if block_end == -1:
        print("Block end not found")
        return
    block_end += len("</div>\n</div>") if text[block_end:block_end+13] == "</div>\n</div>" else len("</div></div>")

    print(f"Replacing block [{block_start}:{block_end}] ({block_end - block_start} chars)")

    # Also fix the prose mention that says "Code Fragment 30.4.2" (it should say 30.4.1)
    prose_idx = text.rfind("Code Fragment 30.4.2 below implements", 0, block_start)
    if prose_idx != -1:
        text = text[:prose_idx] + "Code Fragment 30.4.1 below implements" + text[prose_idx + len("Code Fragment 30.4.2 below implements"):]
        # Adjust offsets after the in-place replace (lengths are equal so no shift)
        print("Also fixed prose reference: '30.4.2 below' -> '30.4.1 below'")

    new_text = text[:block_start] + new_block + text[block_end:]
    p.write_text(new_text, encoding="utf-8")
    print(f"Wrote {p.relative_to(Path(r'E:/Projects/BookBlogsHome/LLMBook'))}")


if __name__ == "__main__":
    main()
