# Load synthetic data and apply multi-stage quality filtering
# Combine rule-based checks with LLM-based quality scoring
import json
from openai import OpenAI
from dataclasses import dataclass

client = OpenAI()


@dataclass
class QualityScore:
    instruction_clarity: int
    response_quality: int
    alignment: int
    complexity: int
    safety_pass: bool
    reasoning: str

    @property
    def composite(self) -> float:
        """Weighted composite score (excluding safety, which is binary)."""
        if not self.safety_pass:
            return 0.0
        return (
            0.20 * self.instruction_clarity +
            0.35 * self.response_quality +
            0.25 * self.alignment +
            0.20 * self.complexity
        ) / 5.0  # Normalize to 0-1


def score_example(instruction: str, response: str,
                  model: str = "gpt-4o") -> QualityScore:
    """Score a single instruction-response pair on multiple dimensions."""
    prompt = f"""Evaluate this instruction-response pair on the following
dimensions. Think through each dimension carefully before scoring.

INSTRUCTION: {instruction}
RESPONSE: {response}

Score each dimension:
- instruction_clarity (1-5): Is the instruction clear and unambiguous?
- response_quality (1-5): Is the response accurate, complete, well-organized?
- alignment (1-5): Does the response directly address the instruction?
- complexity (1-5): How challenging is the task? (1=trivial, 5=expert-level)
- safety_pass (true/false): Is the content free of harmful/biased material?

Provide your analysis, then scores as JSON:
{{
    "reasoning": "your analysis of each dimension",
    "instruction_clarity": <1-5>,
    "response_quality": <1-5>,
    "alignment": <1-5>,
    "complexity": <1-5>,
    "safety_pass": <true|false>
}}"""
    # Send chat completion request to the API
    result = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        response_format={"type": "json_object"}
    )
    data = json.loads(result.choices[0].message.content)
    return QualityScore(**data)


def batch_score_dataset(
    dataset: list[dict],
    min_composite: float = 0.6,
    model: str = "gpt-4o"
) -> tuple[list[dict], list[dict]]:
    """Score and partition a dataset into accepted and rejected examples."""
    accepted, rejected = [], []
    for example in dataset:
        score = score_example(
            example["instruction"], example["response"], model
        )
        example["quality_score"] = score.composite
        example["quality_details"] = {
            "clarity": score.instruction_clarity,
            "quality": score.response_quality,
            "alignment": score.alignment,
            "complexity": score.complexity,
            "safety": score.safety_pass,
        }
        if score.composite >= min_composite and score.safety_pass:
            accepted.append(example)
        else:
            rejected.append(example)
    return accepted, rejected


# Example usage
sample_data = [
    {"instruction": "Explain how B-tree indexing works in databases.",
     "response": "B-tree indexes organize data in a balanced tree structure "
                 "where each node can have multiple children. Leaf nodes contain pointers "
                 "to the actual data rows. Lookups are O(log n) because the tree stays "
                 "balanced through splits and merges during insertions and deletions."},
    {"instruction": "Do something.",
     "response": "Sure, I did something."},
]
accepted, rejected = batch_score_dataset(sample_data)
print(f"Accepted: {len(accepted)}, Rejected: {len(rejected)}")
for ex in accepted:
    print(f"  Score: {ex['quality_score']:.3f} | {ex['instruction'][:50]}...")
