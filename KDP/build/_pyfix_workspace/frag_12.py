import json
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class TopicContext:
    """Context for a single conversation topic."""
    topic_name: str
    summary: str = ""
    turns: list[dict] = field(default_factory=list)
    state: dict = field(default_factory=dict)
    is_resolved: bool = False


class TopicManager:
    """Manages topic tracking and switching in conversations."""

    def __init__(self):
        self.topic_stack: list[TopicContext] = []
        self.resolved_topics: list[TopicContext] = []

    def detect_topic_change(self, user_message: str,
                            current_topic: Optional[TopicContext]) -> dict:
        """Detect if the user is switching, resuming, or staying on topic."""
        current_name = current_topic.topic_name if current_topic else "None"
        saved_topics = (
            [t.topic_name for t in self.topic_stack[:-1]]
            if len(self.topic_stack) > 1
            else []
        )
        prompt = f"""Given the current conversation topic and the user's new message,
determine the topic action.

Current topic: {current_name}
Saved (paused) topics: {saved_topics}

User message: "{user_message}"

Return JSON with:
- action: "continue" (same topic), "switch" (new topic), "resume" (back to saved topic)
- topic_name: name of the topic (new name if switch, existing if resume)
- reason: brief explanation"""
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0
        )
        return json.loads(response.choices[0].message.content)

    def switch_topic(self, new_topic_name: str) -> TopicContext:
        """Switch to a new topic, preserving the current one."""
        new_topic = TopicContext(topic_name=new_topic_name)
        self.topic_stack.append(new_topic)
        return new_topic

    def resume_topic(self, topic_name: str) -> Optional[TopicContext]:
        """Resume a previously paused topic."""
        for i, topic in enumerate(self.topic_stack):
            if topic.topic_name == topic_name:
                # Move to top of stack
                resumed = self.topic_stack.pop(i)
                self.topic_stack.append(resumed)
                return resumed
        return None

    def get_current_topic(self) -> Optional[TopicContext]:
        """Return the currently active topic."""
        return self.topic_stack[-1] if self.topic_stack else None

    def get_topic_context_string(self) -> str:
        """Generate context about active and paused topics."""
        if not self.topic_stack:
            return "No active topics."
        current = self.topic_stack[-1]
        parts = [f"Current topic: {current.topic_name}"]
        if current.summary:
            parts.append(f"Topic context: {current.summary}")
        paused = self.topic_stack[:-1]
        if paused:
            paused_names = [t.topic_name for t in paused]
            parts.append(f"Paused topics: {', '.join(paused_names)}")
        return " | ".join(parts)
