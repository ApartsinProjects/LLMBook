import json
from datetime import datetime
from pathlib import Path


class UserProfileManager:
    """Manages persistent user profiles across sessions."""

    def __init__(self, storage_dir: str = "./user_profiles"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)

    def load_profile(self, user_id: str) -> dict:
        """Load or create a user profile."""
        profile_path = self.storage_dir / f"{user_id}.json"
        if profile_path.exists():
            with open(profile_path) as f:
                return json.load(f)
        return self._create_default_profile(user_id)

    def save_profile(self, user_id: str, profile: dict) -> None:
        """Persist the user profile to disk."""
        profile["last_updated"] = datetime.now().isoformat()
        profile_path = self.storage_dir / f"{user_id}.json"
        with open(profile_path, "w") as f:
            json.dump(profile, f, indent=2)

    def update_from_conversation(self, user_id: str,
                                 conversation: list[dict]) -> dict:
        """Extract profile updates from a completed conversation."""
        profile = self.load_profile(user_id)
        # Use LLM to extract profile-worthy information
        extraction_prompt = f"""Analyze this conversation and extract any new
information about the user that should be remembered for future sessions.

Current profile:
{json.dumps(profile['preferences'], indent=2)}

Conversation:
{self._format_conversation(conversation)}

Return JSON with two fields:
- "new_preferences": dict of any new preferences discovered
- "new_facts": list of new biographical/contextual facts
- "corrections": dict of any corrections to existing profile data

Only include genuinely new or corrected information."""
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": extraction_prompt}],
            response_format={"type": "json_object"},
            temperature=0
        )
        updates = json.loads(response.choices[0].message.content)
        # Apply updates
        if updates.get("new_preferences"):
            profile["preferences"].update(updates["new_preferences"])
        if updates.get("new_facts"):
            profile["facts"].extend(updates["new_facts"])
        if updates.get("corrections"):
            profile["preferences"].update(updates["corrections"])
        # Update session count
        profile["session_count"] += 1
        profile["last_session"] = datetime.now().isoformat()
        self.save_profile(user_id, profile)
        return profile

    def get_context_string(self, user_id: str) -> str:
        """Generate a context string for inclusion in system prompts."""
        profile = self.load_profile(user_id)
        parts = [f"Returning user (session #{profile['session_count']})."]
        if profile["preferences"]:
            prefs = "; ".join(
                f"{k}: {v}" for k, v in profile["preferences"].items()
            )
            parts.append(f"Known preferences: {prefs}")
        if profile["facts"]:
            parts.append("Known facts: " + "; ".join(profile["facts"][-5:]))
        return " ".join(parts)

    def _create_default_profile(self, user_id: str) -> dict:
        return {
            "user_id": user_id,
            "created": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "last_session": None,
            "session_count": 0,
            "preferences": {},
            "facts": [],
            "interaction_style": {}
        }

    @staticmethod
    def _format_conversation(conversation: list[dict]) -> str:
        return "\n".join(
            f"{m['role'].title()}: {m['content']}"
            for m in conversation
        )
