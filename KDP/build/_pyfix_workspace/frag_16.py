from dataclasses import dataclass


@dataclass
class TestCase:
    """A single golden test case for prompt regression testing."""
    input_text: str
    expected_criteria: dict[str, str]  # criterion_name -> description
    category: str = "general"


@dataclass
class RegressionResult:
    """Comparison between baseline and candidate prompt performance."""
    total_cases: int
    improved: int
    regressed: int
    unchanged: int
    regression_rate: float
    details: list[dict]


class PromptRegressionTester:
    """Run regression tests when prompts change."""

    def __init__(self, eval_fn, golden_tests: list[TestCase]):
        """
        Args:
            eval_fn: function(prompt, input_text) -> dict of scores
            golden_tests: curated test cases with expected criteria
        """
        self.eval_fn = eval_fn
        self.golden_tests = golden_tests

    def run_comparison(
        self,
        baseline_prompt: str,
        candidate_prompt: str,
        regression_threshold: float = 0.05,
    ) -> RegressionResult:
        """Compare candidate prompt against baseline on golden tests."""
        details = []
        improved = regressed = unchanged = 0
        for test in self.golden_tests:
            baseline_result = self.eval_fn(baseline_prompt, test.input_text)
            candidate_result = self.eval_fn(candidate_prompt, test.input_text)
            baseline_score = sum(baseline_result.values()) / len(baseline_result)
            candidate_score = sum(candidate_result.values()) / len(candidate_result)
            diff = candidate_score - baseline_score
            if diff > regression_threshold:
                improved += 1
                status = "improved"
            elif diff < -regression_threshold:
                regressed += 1
                status = "regressed"
            else:
                unchanged += 1
                status = "unchanged"
            details.append({
                "input": test.input_text[:80],
                "category": test.category,
                "baseline_score": round(baseline_score, 3),
                "candidate_score": round(candidate_score, 3),
                "status": status,
            })
        total = len(self.golden_tests)
        return RegressionResult(
            total_cases=total,
            improved=improved,
            regressed=regressed,
            unchanged=unchanged,
            regression_rate=round(regressed / total, 3) if total > 0 else 0.0,
            details=details,
        )
