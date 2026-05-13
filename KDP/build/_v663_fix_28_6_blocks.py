"""One-shot fix: replace the two over-flattened code blocks in
section-28.6.html with hand-corrected versions.

These blocks have multi-level nested control structures (try/except inside
for inside def, etc.) that the auto-fixer in _v662 cannot recover. Hand-
rewriting once is faster than tuning the heuristic.
"""
import ast
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
TARGET = ROOT / 'part-8-evaluation-production' / 'module-28-production-engineering' / 'section-28.6.html'

FIXED_1 = '''import random
import asyncio
from typing import TypeVar, Callable, Awaitable

T = TypeVar("T")

async def retry_with_budget(
    fn: Callable[..., Awaitable[T]],
    *args,
    max_attempts: int = 5,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0,
    jitter: float = 0.3,
    max_cost_usd: float = 1.0,
    cost_tracker: "CostTracker | None" = None,
    **kwargs,
) -> T:
    """Retry with jittered exponential backoff and budget awareness.

    Stops retrying if cumulative cost exceeds the budget threshold,
    preventing runaway spend on requests that consistently fail
    after consuming tokens (e.g., partial streaming responses).
    """
    delay = initial_delay
    last_exception = None

    for attempt in range(1, max_attempts + 1):
        # Budget gate: stop if we have already spent too much
        if cost_tracker and cost_tracker.total_cost > max_cost_usd:
            raise BudgetExceededError(
                f"Retry budget exhausted: ${cost_tracker.total_cost:.4f} "
                f"exceeds ${max_cost_usd:.2f} limit after {attempt - 1} attempts"
            )

        try:
            return await fn(*args, **kwargs)
        except RateLimitError as e:
            last_exception = e
            # Respect Retry-After header if present
            delay = max(delay, get_retry_after(e))
        except (TimeoutError, ConnectionError) as e:
            last_exception = e
        except ContextWindowOverflowError:
            # Not transient: retrying the same input will always fail
            raise

        if attempt < max_attempts:
            jittered_delay = delay * (1 + random.uniform(-jitter, jitter))
            await asyncio.sleep(jittered_delay)
            delay *= backoff_factor

    raise MaxRetriesExceededError(
        f"Failed after {max_attempts} attempts"
    ) from last_exception
'''

FIXED_2 = '''@workflow.defn
class BookingWorkflow:
    """Saga pattern: each step registers a compensation action."""

    @workflow.run
    async def run(self, request: TravelRequest) -> BookingResult:
        compensations: list[tuple[str, dict]] = []

        try:
            # Step 1: Book flight
            flight = await workflow.execute_activity(
                book_flight, request.flight_details,
                start_to_close_timeout=timedelta(seconds=60),
            )
            compensations.append(("cancel_flight", {"id": flight.id}))

            # Step 2: Book hotel
            hotel = await workflow.execute_activity(
                book_hotel, request.hotel_details,
                start_to_close_timeout=timedelta(seconds=60),
            )
            compensations.append(("cancel_hotel", {"id": hotel.id}))

            # Step 3: LLM generates itinerary summary
            itinerary = await workflow.execute_activity(
                generate_itinerary,
                args=[flight, hotel, request.preferences],
                start_to_close_timeout=timedelta(seconds=120),
            )

            return BookingResult(
                flight=flight, hotel=hotel, itinerary=itinerary
            )

        except Exception as e:
            # Execute compensations in reverse order
            for comp_name, comp_args in reversed(compensations):
                await workflow.execute_activity(
                    comp_name, comp_args,
                    start_to_close_timeout=timedelta(seconds=30),
                )
            raise WorkflowFailedError(f"Booking failed: {e}") from e
'''

# Validate
ast.parse(FIXED_1)
ast.parse(FIXED_2)

text = TARGET.read_text(encoding='utf-8')
BLOCK_RE = re.compile(r'(<pre[^>]*>\s*<code[^>]*\b(?:lang|language)-python\b[^>]*>)([\s\S]*?)(</code>\s*</pre>)', re.IGNORECASE)

new_chunks = []
last = 0
n = 0
for m in BLOCK_RE.finditer(text):
    line = text[:m.start()].count('\n') + 1
    if line == 461:
        new_chunks.append(text[last:m.start()])
        new_chunks.append(f'<pre><code class="language-python">{html.escape(FIXED_1.rstrip())}</code></pre>')
        last = m.end()
        n += 1
    elif line == 552:
        new_chunks.append(text[last:m.start()])
        new_chunks.append(f'<pre><code class="language-python">{html.escape(FIXED_2.rstrip())}</code></pre>')
        last = m.end()
        n += 1
new_chunks.append(text[last:])
TARGET.write_text(''.join(new_chunks), encoding='utf-8')
print(f'Replaced {n} blocks in {TARGET.name}')
