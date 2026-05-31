import json
from openai import OpenAI

client = OpenAI()


class CoWritingAssistant:
    """AI co-writing partner with style adaptation capabilities."""

    def __init__(self):
        self.writing_style: dict = {}
        self.story_context: dict = {
            "characters": [],
            "plot_points": [],
            "setting": "",
            "tone": "",
            "genre": ""
        }

    def analyze_writing_style(self, sample_text: str) -> dict:
        """Analyze a text sample to extract the author's style."""
        analysis_prompt = """Analyze the writing style of this text sample.
Return a JSON object with these fields:
- sentence_structure: "simple", "complex", "varied", "fragmented"
- vocabulary_level: "plain", "moderate", "literary", "experimental"
- tone: the overall emotional quality
- pacing: "fast", "moderate", "slow", "varied"
- perspective: "first_person", "second_person", "third_limited", "third_omniscient"
- distinctive_features: list of 3-5 specific stylistic habits
- dialogue_style: how characters speak
- description_density: "sparse", "moderate", "rich", "ornate"

Text sample:
\"\"\"
{text}
\"\"\"

Return valid JSON only."""
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{
                "role": "user",
                "content": analysis_prompt.format(text=sample_text)
            }],
            response_format={"type": "json_object"},
            temperature=0.3
        )
        self.writing_style = json.loads(
            response.choices[0].message.content
        )
        return self.writing_style

    def continue_draft(self, draft_so_far: str,
                       instruction: str = "Continue naturally",
                       words: int = 200) -> str:
        """Continue a draft in the established writing style."""
        style_desc = "\n".join(
            f"- {k}: {v}" for k, v in self.writing_style.items()
        )
        prompt = f"""You are a co-writing assistant. Continue the draft below,
matching the established writing style precisely.

## Writing Style to Match
{style_desc}

## Story Context
Genre: {self.story_context.get('genre', 'Not specified')}
Setting: {self.story_context.get('setting', 'Not specified')}
Tone: {self.story_context.get('tone', 'Not specified')}

## Instruction
{instruction}

## Draft So Far
{draft_so_far}

## Continue
Write approximately {words} words. Match the style exactly.
Do not add meta-commentary. Just continue the story."""
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            max_tokens=words * 2
        )
        return response.choices[0].message.content

    def suggest_alternatives(self, passage: str, count: int = 3) -> list:
        """Generate alternative phrasings for a passage."""
        prompt = f"""Rewrite this passage in {count} different ways,
maintaining the same meaning and approximate style but exploring
different word choices, sentence structures, or emphases.

Original:
\"\"\"{passage}\"\"\"

Return each alternative numbered 1-{count}."""
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9
        )
        return response.choices[0].message.content
