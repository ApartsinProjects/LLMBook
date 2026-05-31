from openai import OpenAI
from enum import Enum
import json

client = OpenAI()


class ClarificationType(Enum):
    NONE_NEEDED = "none_needed"
    AMBIGUOUS_REFERENCE = "ambiguous_reference"
    MISSING_INFORMATION = "missing_information"
    CONFLICTING_REQUEST = "conflicting_request"
    OUT_OF_SCOPE = "out_of_scope"
    UNCLEAR_INTENT = "unclear_intent"


def detect_clarification_need(
    user_message: str,
    conversation_history: list[dict],
    available_actions: list[str]
) -> dict:
    """Determine if clarification is needed before proceeding."""
    prompt = f"""Analyze whether this user message needs clarification
before the system can act. Consider the conversation history.

Available system actions: {', '.join(available_actions)}

Conversation history (last 3 turns):
{json.dumps(conversation_history[-6:], indent=2)}

Current user message: "{user_message}"

Return JSON with:
- needs_clarification: true/false
- type: one of [none_needed, ambiguous_reference, missing_information,
  conflicting_request, out_of_scope, unclear_intent]
- confidence: 0.0 to 1.0 (how confident the system is in its interpretation)
- best_interpretation: what the system thinks the user means
- clarification_question: question to ask if clarification needed
- alternatives: list of possible interpretations (if ambiguous)"""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        temperature=0
    )
    return json.loads(response.choices[0].message.content)


class ConversationRepairManager:
    """Handles clarification, correction, and repair in dialogue."""

    def __init__(self, confidence_threshold: float = 0.75):
        self.confidence_threshold = confidence_threshold
        self.pending_clarification: dict = None
        self.correction_history: list[dict] = []

    def process_message(self, user_message: str, history: list,
                        actions: list[str]) -> dict:
        """Decide whether to act, clarify, or handle a correction."""
        # Check if this is a correction of something previous
        if self._is_correction(user_message, history):
            return self._handle_correction(user_message, history)
        # Check if this answers a pending clarification
        if self.pending_clarification:
            return self._resolve_clarification(user_message)
        # Analyze the new message
        analysis = detect_clarification_need(
            user_message, history, actions
        )
        if (analysis["needs_clarification"]
                and analysis["confidence"] < self.confidence_threshold):
            self.pending_clarification = analysis
            return {
                "action": "clarify",
                "question": analysis["clarification_question"],
                "alternatives": analysis.get("alternatives", [])
            }
        return {
            "action": "proceed",
            "interpretation": analysis["best_interpretation"],
            "confidence": analysis["confidence"]
        }

    def _is_correction(self, message: str, history: list) -> bool:
        """Detect if the user is correcting a previous statement."""
        correction_markers = [
            "no, i meant", "actually,", "sorry, i meant",
            "not that", "i said", "no no", "correction:",
            "let me rephrase", "what i meant was",
            "change that to", "instead of"
        ]
        lower = message.lower().strip()
        return any(lower.startswith(m) for m in correction_markers)

    def _handle_correction(self, message: str, history: list) -> dict:
        """Process a user correction and update state."""
        self.correction_history.append({
            "original_context": history[-2:] if len(history) >= 2 else [],
            "correction": message
        })
        return {
            "action": "correct",
            "message": message,
            "instruction": (
                "The user is correcting their previous statement. "
                "Update your understanding accordingly."
            )
        }

    def _resolve_clarification(self, answer: str) -> dict:
        """Resolve a pending clarification with the user's answer."""
        resolved = {
            "action": "proceed",
            "original_question": self.pending_clarification,
            "clarification_answer": answer,
            "interpretation": (
                f"Original: {self.pending_clarification['best_interpretation']}. "
                f"Clarified with: {answer}"
            )
        }
        self.pending_clarification = None
        return resolved
