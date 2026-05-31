from dataclasses import dataclass, field
from typing import Optional


@dataclass
class GateResult:
    """Result of a quality gate evaluation."""
    gate_name: str
    passed: bool
    overall_score: float
    threshold: float
    category_scores: dict[str, float] = field(default_factory=dict)
    regressions: list[str] = field(default_factory=list)
    details: str = ""


class QualityGate:
    """Automated quality gate for LLM deployment pipelines."""

    def __init__(
        self,
        gate_name: str,
        overall_threshold: float = 0.85,
        category_thresholds: Optional[dict[str, float]] = None,
        max_regression: float = 0.03,
    ):
        self.gate_name = gate_name
        self.overall_threshold = overall_threshold
        self.category_thresholds = category_thresholds or {}
        self.max_regression = max_regression

    def check_gate(
        self,
        scores: dict[str, list[float]],
        baseline_scores: Optional[dict[str, list[float]]] = None,
    ) -> GateResult:
        """Evaluate whether the candidate passes the quality gate.

        Args:
            scores: category_name -> list of scores for that category
            baseline_scores: previous production scores for regression check
        """
        # Compute category-level means
        category_means = {
            cat: sum(vals) / len(vals)
            for cat, vals in scores.items() if vals
        }
        # Compute overall mean across all scores
        all_scores = [s for vals in scores.values() for s in vals]
        overall = sum(all_scores) / len(all_scores) if all_scores else 0.0
        # Check for regressions against baseline
        regressions = []
        if baseline_scores:
            for cat, vals in baseline_scores.items():
                baseline_mean = sum(vals) / len(vals) if vals else 0.0
                current_mean = category_means.get(cat, 0.0)
                drop = baseline_mean - current_mean
                if drop > self.max_regression:
                    regressions.append(
                        f"{cat}: dropped {drop:.3f} "
                        f"(baseline {baseline_mean:.3f} "
                        f"-> current {current_mean:.3f})"
                    )
        # Check category-level thresholds
        category_failures = []
        for cat, threshold in self.category_thresholds.items():
            if cat in category_means and category_means[cat] < threshold:
                category_failures.append(
                    f"{cat}: {category_means[cat]:.3f} < {threshold}"
                )
        passed = (
            overall >= self.overall_threshold
            and len(regressions) == 0
            and len(category_failures) == 0
        )
        details_parts = []
        if regressions:
            details_parts.append(
                "Regressions: " + "; ".join(regressions)
            )
        if category_failures:
            details_parts.append(
                "Category failures: " + "; ".join(category_failures)
            )
        return GateResult(
            gate_name=self.gate_name,
            passed=passed,
            overall_score=round(overall, 4),
            threshold=self.overall_threshold,
            category_scores={k: round(v, 4) for k, v in category_means.items()},
            regressions=regressions,
            details=" | ".join(details_parts) if details_parts else "All checks passed",
        )


# Example: pre-deployment quality gate
gate = QualityGate(
    gate_name="pre-deploy",
    overall_threshold=0.85,
    category_thresholds={"safety": 0.95, "factuality": 0.80},
    max_regression=0.03,
)
candidate_scores = {
    "safety": [1.0, 1.0, 0.95, 1.0, 0.90],
    "factuality": [0.85, 0.90, 0.80, 0.88, 0.82],
    "helpfulness": [0.78, 0.82, 0.85, 0.80, 0.76],
}
baseline_scores = {
    "safety": [1.0, 1.0, 1.0, 0.95, 1.0],
    "factuality": [0.82, 0.85, 0.80, 0.84, 0.81],
    "helpfulness": [0.80, 0.83, 0.81, 0.79, 0.82],
}
result = gate.check_gate(candidate_scores, baseline_scores)
print(f"Gate: {result.gate_name}")
print(f"Passed: {result.passed}")
print(f"Overall score: {result.overall_score}")
print(f"Category scores: {result.category_scores}")
print(f"Details: {result.details}")
