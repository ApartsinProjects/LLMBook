# implement perturbation_contamination_test, evaluate_set
import numpy as np
from typing import Callable


def perturbation_contamination_test(
    model_fn: Callable,
    original_questions: list[dict],
    perturbed_questions: list[dict],
    threshold: float = 0.15
) -> dict:
    """Detect benchmark contamination via perturbation analysis.

    If accuracy drops sharply on minor rephrasing, the model may
    have memorized the original questions rather than learned the skill.

    Args:
        model_fn: callable that takes a question and returns an answer
        original_questions: list of {'question': str, 'answer': str}
        perturbed_questions: rephrased versions with same answers
        threshold: max acceptable accuracy drop (larger drops = contamination)
    """
    def evaluate_set(questions):
        correct = 0
        for q in questions:
            prediction = model_fn(q["question"])
            if prediction.strip().lower() == q["answer"].strip().lower():
                correct += 1
        return correct / len(questions)

    orig_acc = evaluate_set(original_questions)
    pert_acc = evaluate_set(perturbed_questions)
    drop = orig_acc - pert_acc
    return {
        "original_accuracy": round(orig_acc, 4),
        "perturbed_accuracy": round(pert_acc, 4),
        "accuracy_drop": round(drop, 4),
        "contamination_suspected": drop > threshold,
        "message": (
            "Contamination likely: large accuracy drop on minor rephrasing"
            if drop > threshold
            else "No strong contamination signal detected"
        )
    }
