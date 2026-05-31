# Verifiable reward functions for different domains
import subprocess
import json
import re
from typing import Optional


def math_reward(
    model_answer: str,
    ground_truth: str,
    tolerance: float = 1e-6,
) -> float:
    """Binary reward for math: 1.0 if correct, 0.0 otherwise."""
    # Extract numerical answer from model output
    extracted = extract_final_answer(model_answer)
    if extracted is None:
        return 0.0
    try:
        model_val = float(extracted)
        truth_val = float(ground_truth)
        return 1.0 if abs(model_val - truth_val) < tolerance else 0.0
    except ValueError:
        # String comparison for symbolic answers
        return 1.0 if extracted.strip() == ground_truth.strip() else 0.0


def code_reward(
    generated_code: str,
    test_cases: list,
    timeout: int = 10,
) -> float:
    """Graded reward for code: fraction of tests passed."""
    passed = 0
    for test in test_cases:
        full_code = generated_code + "\n" + test["test_code"]
        try:
            result = subprocess.run(
                ["python", "-c", full_code],
                capture_output=True,
                timeout=timeout,
                text=True,
            )
            if result.returncode == 0:
                passed += 1
        except subprocess.TimeoutExpired:
            continue
    return passed / len(test_cases) if test_cases else 0.0


def proof_reward(
    proof_text: str,
    theorem_statement: str,
    lean_project_path: str,
) -> float:
    """Binary reward for Lean 4 proofs."""
    # Write proof to a temporary Lean file
    lean_code = f"{theorem_statement}\n{proof_text}"
    with open(f"{lean_project_path}/Temp.lean", "w") as f:
        f.write(lean_code)
    result = subprocess.run(
        ["lake", "build", "Temp"],
        capture_output=True,
        cwd=lean_project_path,
        timeout=60,
    )
    return 1.0 if result.returncode == 0 else 0.0


def extract_final_answer(text: str) -> Optional[str]:
    """Extract boxed answer from math response."""
    # Look for \boxed{...} or "The answer is ..."
    boxed = re.findall(r"\\boxed\{([^}]+)\}", text)
    if boxed:
        return boxed[-1]
    answer_pattern = re.findall(
        r"(?:the answer is|therefore|thus)[:\s]+([^\n.]+)",
        text, re.IGNORECASE,
    )
    if answer_pattern:
        return answer_pattern[-1].strip()
    return None
