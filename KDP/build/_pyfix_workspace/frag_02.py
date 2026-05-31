# Estimate token usage and API cost for different model configurations
# Token counting enables accurate cost projections before running at scale
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import defaultdict


@dataclass
class UsageRecord:
    timestamp: datetime
    model: str
    feature: str
    input_tokens: int
    output_tokens: int
    cost: float
    latency_ms: float


class CostMonitor:
    """Track LLM usage and alert on anomalies."""

    def __init__(self, daily_budget: float = 100.0):
        self.records: list[UsageRecord] = []
        self.daily_budget: float = daily_budget
        self.alerts: list[str] = []

    def record(self, model: str, feature: str,
               input_tokens: int, output_tokens: int,
               cost: float, latency_ms: float):
        self.records.append(UsageRecord(
            datetime.now(), model, feature,
            input_tokens, output_tokens, cost, latency_ms
        ))
        self._check_alerts()

    def _check_alerts(self):
        today = datetime.now().date()
        today_cost = sum(
            r.cost for r in self.records
            if r.timestamp.date() == today
        )
        if today_cost > self.daily_budget * 0.8:
            self.alerts.append(
                f"WARNING: Daily spend ${today_cost:.2f} "
                f"exceeds 80% of budget ${self.daily_budget:.2f}"
            )

    def dashboard(self) -> str:
        by_model = defaultdict(lambda: {"cost": 0, "calls": 0, "tokens": 0})
        by_feature = defaultdict(lambda: {"cost": 0, "calls": 0})
        for r in self.records:
            by_model[r.model]["cost"] += r.cost
            by_model[r.model]["calls"] += 1
            by_model[r.model]["tokens"] += r.input_tokens + r.output_tokens
            by_feature[r.feature]["cost"] += r.cost
            by_feature[r.feature]["calls"] += 1
        total_cost = sum(m["cost"] for m in by_model.values())
        total_calls = sum(m["calls"] for m in by_model.values())
        lines = [
            "LLM Cost Dashboard",
            "=" * 55,
            f"Total cost: ${total_cost:.4f} | Total calls: {total_calls}",
            "",
            "By Model:",
        ]
        for model, stats in sorted(by_model.items(),
                                   key=lambda x: x[1]["cost"], reverse=True):
            pct = stats["cost"] / total_cost * 100 if total_cost > 0 else 0
            lines.append(
                f"  {model:<22} ${stats['cost']:>8.4f} "
                f"({pct:4.1f}%) {stats['calls']:>4} calls"
            )
        lines.append("\nBy Feature:")
        for feature, stats in sorted(by_feature.items(),
                                     key=lambda x: x[1]["cost"], reverse=True):
            lines.append(
                f"  {feature:<22} ${stats['cost']:>8.4f} "
                f"{stats['calls']:>4} calls"
            )
        if self.alerts:
            lines.append(f"\nAlerts ({len(self.alerts)}):")
            for alert in self.alerts[-3:]:
                lines.append(f"  {alert}")
        return "\n".join(lines)


# Simulate a day of usage
monitor = CostMonitor(daily_budget=50.0)
import random
random.seed(42)
features = ["classification", "summarization", "extraction", "chat"]
models = [
    ("gpt-4o-mini", 0.003),
    ("gpt-4o", 0.012),
    ("claude-opus", 0.025),
]
for _ in range(200):
    model, base_cost = random.choice(models)
    feature = random.choice(features)
    cost = base_cost * (0.5 + random.random())
    monitor.record(
        model=model, feature=feature,
        input_tokens=random.randint(100, 2000),
        output_tokens=random.randint(50, 500),
        cost=cost,
        latency_ms=random.uniform(50, 1000),
    )
print(monitor.dashboard())
