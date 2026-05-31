from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Callable, Optional


@dataclass
class EvalCycleResult:
    """Result of a single continuous evaluation cycle."""
    timestamp: str
    gate_result: dict
    samples_evaluated: int
    alert_triggered: bool
    alert_message: str = ""


class ContinuousEvalScheduler:
    """Schedule periodic evaluation of production LLM outputs."""

    def __init__(
        self,
        sample_fn: Callable[[], list[dict]],
        eval_fn: Callable[[dict], dict[str, float]],
        gate: "QualityGate",
        baseline_scores: Optional[dict[str, list[float]]] = None,
    ):
        """
        Args:
            sample_fn: returns recent production request/response pairs
            eval_fn: scores a single request/response pair
            gate: QualityGate instance for threshold checking
            baseline_scores: production baseline for regression detection
        """
        self.sample_fn = sample_fn
        self.eval_fn = eval_fn
        self.gate = gate
        self.baseline_scores = baseline_scores
        self.history: list[EvalCycleResult] = []

    def run_evaluation_cycle(self) -> EvalCycleResult:
        """Run one evaluation cycle on sampled production traffic."""
        samples = self.sample_fn()
        if not samples:
            return EvalCycleResult(
                timestamp=datetime.now(timezone.utc).isoformat(),
                gate_result={},
                samples_evaluated=0,
                alert_triggered=False,
                alert_message="No samples available",
            )
        # Evaluate each sample and group scores by category
        category_scores: dict[str, list[float]] = {}
        for sample in samples:
            scores = self.eval_fn(sample)
            for category, score in scores.items():
                category_scores.setdefault(category, []).append(score)
        # Run through the quality gate
        gate_result = self.gate.check_gate(
            category_scores, self.baseline_scores
        )
        alert = not gate_result.passed
        cycle = EvalCycleResult(
            timestamp=datetime.now(timezone.utc).isoformat(),
            gate_result={
                "passed": gate_result.passed,
                "overall_score": gate_result.overall_score,
                "category_scores": gate_result.category_scores,
                "regressions": gate_result.regressions,
            },
            samples_evaluated=len(samples),
            alert_triggered=alert,
            alert_message=gate_result.details if alert else "",
        )
        self.history.append(cycle)
        return cycle

    def get_trend(self, last_n: int = 7) -> list[float]:
        """Return recent overall scores for trend analysis."""
        recent = self.history[-last_n:] if self.history else []
        return [
            h.gate_result.get("overall_score", 0.0)
            for h in recent
            if h.gate_result
        ]
