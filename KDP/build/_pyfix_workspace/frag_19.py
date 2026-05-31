import time
import json
import re
from dataclasses import dataclass
from typing import Callable


@dataclass
class GuardrailResult:
    passed: bool
    guardrail_name: str
    details: str = ""
    latency_ms: float = 0.0


class GuardrailPipeline:
    """Centralized input/output validation for LLM applications."""

    def __init__(self):
        self.input_guardrails: list = []
        self.output_guardrails: list = []

    def add_input_guardrail(self, name: str, check_fn: Callable[[str], GuardrailResult]):
        self.input_guardrails.append((name, check_fn))

    def add_output_guardrail(self, name: str, check_fn: Callable[[str, str], GuardrailResult]):
        self.output_guardrails.append((name, check_fn))

    def validate_input(self, user_input: str) -> list[GuardrailResult]:
        results = []
        for name, check_fn in self.input_guardrails:
            start = time.monotonic()
            result = check_fn(user_input)
            result.latency_ms = (time.monotonic() - start) * 1000
            results.append(result)
            if not result.passed:
                break  # fail fast on first input guardrail failure
        return results

    def validate_output(self, prompt: str, response: str) -> list[GuardrailResult]:
        results = []
        for name, check_fn in self.output_guardrails:
            start = time.monotonic()
            result = check_fn(prompt, response)
            result.latency_ms = (time.monotonic() - start) * 1000
            results.append(result)
        return results


# Example guardrails
def prompt_injection_check(user_input: str) -> GuardrailResult:
    """Detect common prompt injection patterns."""
    injection_patterns = [
        r"ignore\s+(all\s+)?previous\s+instructions",
        r"you\s+are\s+now\s+",
        r"system\s*:\s*",
        r"<\|im_start\|>",
    ]
    for pattern in injection_patterns:
        if re.search(pattern, user_input, re.IGNORECASE):
            return GuardrailResult(
                passed=False,
                guardrail_name="prompt_injection",
                details=f"Matched injection pattern: {pattern}",
            )
    return GuardrailResult(passed=True, guardrail_name="prompt_injection")


def json_schema_check(prompt: str, response: str) -> GuardrailResult:
    """Validate that JSON responses conform to expected schema."""
    try:
        parsed = json.loads(response)
        if not isinstance(parsed, dict):
            return GuardrailResult(
                passed=False,
                guardrail_name="json_schema",
                details="Response is valid JSON but not an object",
            )
        return GuardrailResult(passed=True, guardrail_name="json_schema")
    except json.JSONDecodeError as e:
        return GuardrailResult(
            passed=False,
            guardrail_name="json_schema",
            details=f"Invalid JSON: {e}",
        )


# Assembly
pipeline = GuardrailPipeline()
pipeline.add_input_guardrail("prompt_injection", prompt_injection_check)
pipeline.add_output_guardrail("json_schema", json_schema_check)
