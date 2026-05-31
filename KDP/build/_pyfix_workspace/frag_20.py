import asyncio
import time


class BudgetExhausted(Exception):
    pass


class ResilientLLMClient:
    """Production LLM client with retries, fallback, circuit breaker,
    guardrails, and budget controls.
    """

    def __init__(
        self,
        fallback_chain: "FallbackChain",
        circuit_breaker: "LLMCircuitBreaker",
        guardrail_pipeline: "GuardrailPipeline",
        retry_config: "RetryConfig",
        budget_limit_usd: float = 100.0,
    ):
        self.fallback_chain = fallback_chain
        self.circuit_breaker = circuit_breaker
        self.guardrails = guardrail_pipeline
        self.retry_config = retry_config
        self.budget_limit_usd = budget_limit_usd
        self.budget_spent_usd: float = 0.0
        self.request_count: int = 0
        self.slo_tracker = SLOTracker()

    async def complete(
        self,
        prompt: str,
        expected_format: str | None = None,
        cost_per_request: float = 0.01,
    ) -> dict:
        """Send a prompt through the full resilience stack.

        Flow:
            1. Budget check
            2. Input guardrails
            3. Circuit breaker check
            4. Fallback chain with retries
            5. Output guardrails
            6. SLO recording
        """
        start_time = time.monotonic()
        # 1. Budget check
        if self.budget_spent_usd + cost_per_request > self.budget_limit_usd:
            raise BudgetExhausted(
                f"Budget exhausted: ${self.budget_spent_usd:.2f} of "
                f"${self.budget_limit_usd:.2f} spent"
            )
        # 2. Input guardrails
        input_results = self.guardrails.validate_input(prompt)
        for result in input_results:
            if not result.passed:
                return {
                    "response": "Request blocked by input guardrails.",
                    "blocked": True,
                    "guardrail": result.guardrail_name,
                    "details": result.details,
                }
        # 3. Circuit breaker check
        if not self.circuit_breaker.can_execute():
            return await self._fallback_response(prompt, "circuit_open")
        # 4. Call with retries and fallback
        try:
            def response_validator(result):
                if not result or not result.get("response"):
                    return False
                output_results = self.guardrails.validate_output(
                    prompt, result["response"]
                )
                return all(r.passed for r in output_results)

            result = await self.fallback_chain.call(
                prompt, validator=response_validator
            )
            self.circuit_breaker.record_success()
            self.budget_spent_usd += cost_per_request
            self.request_count += 1
            # 6. Record SLO metrics
            latency_ms = (time.monotonic() - start_time) * 1000
            self.slo_tracker.record("availability", 1.0)
            self.slo_tracker.record("ttft_p95_ms", latency_ms)
            is_useful = result.get("provider") not in ("cache", "default")
            self.slo_tracker.record("goodput", 1.0 if is_useful else 0.0)
            result["latency_total_ms"] = latency_ms
            result["budget_remaining_usd"] = self.budget_limit_usd - self.budget_spent_usd
            return result
        except Exception as e:
            self.circuit_breaker.record_failure()
            self.slo_tracker.record("availability", 0.0)
            self.slo_tracker.record("goodput", 0.0)
            return await self._fallback_response(prompt, str(e))

    async def _fallback_response(self, prompt: str, reason: str) -> dict:
        """Return cached or default response when all else fails."""
        cache_key = prompt[:200]
        if cache_key in self.fallback_chain.cache:
            return {
                "response": self.fallback_chain.cache[cache_key],
                "provider": "cache",
                "fallback_reason": reason,
            }
        return {
            "response": self.fallback_chain.default_response,
            "provider": "default",
            "fallback_reason": reason,
        }
