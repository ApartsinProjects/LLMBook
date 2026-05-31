from enum import Enum


class ConversationMode(Enum):
    TASK = "task"
    CHITCHAT = "chitchat"
    FAQ = "faq"
    ESCALATION = "escalation"


def classify_intent(user_message: str, context: list) -> ConversationMode:
    """Route user message to the appropriate dialogue mode."""
    classification_prompt = """Classify the user's intent into one of these categories:
- TASK: User wants to perform a specific action (book, order, cancel, modify, check status)
- CHITCHAT: Casual conversation, greetings, small talk, opinions
- FAQ: Asking a question about products, policies, or general information
- ESCALATION: Requesting a human agent, expressing frustration, threatening

Recent context: {context}
User message: {message}

Respond with exactly one word: TASK, CHITCHAT, FAQ, or ESCALATION"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": classification_prompt.format(
                context=context[-3:] if context else "None",
                message=user_message
            )
        }],
        temperature=0,
        max_tokens=10
    )
    label = response.choices[0].message.content.strip().upper()
    return ConversationMode(label.lower())


class HybridDialogueRouter:
    """Routes conversations between task and freeform modes."""

    def __init__(self):
        self.task_pipeline = None      # TaskDialoguePipeline instance
        self.chitchat_pipeline = None  # OpenDomainPipeline instance
        self.faq_pipeline = None       # RAG-based Q&A
        self.active_mode = None

    def handle_message(self, user_message: str, history: list) -> str:
        mode = classify_intent(user_message, history)
        # If already in a task, stay in task mode unless explicitly leaving
        if (self.active_mode == ConversationMode.TASK
                and mode == ConversationMode.CHITCHAT):
            # Check if the task is still active
            if self.task_pipeline and not self.task_pipeline.is_complete:
                mode = ConversationMode.TASK  # Stay in task mode
        self.active_mode = mode
        if mode == ConversationMode.TASK:
            return self.task_pipeline.process(user_message)
        elif mode == ConversationMode.FAQ:
            return self.faq_pipeline.answer(user_message)
        elif mode == ConversationMode.ESCALATION:
            return self._handle_escalation(user_message)
        else:
            return self.chitchat_pipeline.respond(user_message)

    def _handle_escalation(self, message: str) -> str:
        return ("I understand your concern. Let me connect you with "
                "a human agent who can help further. Please hold.")
