---
name: Dependency Management
description: Managing external dependencies safely with circuit breakers, timeouts, retries with exponential backoff, bulkhead pattern, graceful degradation, and dependency isolation.
leadership_principles:
  - Ownership
  - Think Big
  - Insist on the Highest Standards
---

## Overview

Every external dependency is a liability. Every network call can fail, every downstream service can become slow, every database can become overloaded. Dependency management is the discipline of treating every external interaction as unreliable and building defenses that keep your service healthy even when dependencies are not.

At Amazon, a single service may depend on dozens of other services, databases, caches, and external APIs. Without proper dependency management, a slowdown in one dependency cascades into a full system outage—the "thundering herd" or "retry storm" that has caused some of Amazon's most significant incidents.

The core principle: **your service's availability is the product of its dependencies' availabilities, unless you actively decouple from them.** If you depend on 5 services each at 99.9% availability and do nothing, your service can only be 99.5% available. Proper dependency management breaks this multiplication.

## When to Use

- Making any HTTP call to another service
- Querying any database or cache
- Calling any third-party API
- Publishing to or consuming from message queues
- Reading from configuration services
- Any I/O operation that crosses a network boundary

## Amazon Context

Amazon's distributed architecture means most requests traverse multiple services. The call graph for a single customer request might involve 50+ services. Without dependency isolation, a single slow service can cause a cascading failure that takes down the entire customer experience.

Key lessons learned:
- **The 2004 outage** taught Amazon that retries without backoff amplify failures (retry storms)
- **The "thundering herd" incidents** taught that all callers recovering simultaneously overwhelms the recovering service
- **The "gray failures"** (slow but not dead services) are harder to detect and more damaging than hard failures

Amazon's architecture mandates: circuit breakers at every service boundary, timeouts on every call, retries with jitter, and bulkheads isolating failure domains. These are not optional patterns—they are architectural requirements enforced through ORR.

## The Process

### 1. Timeouts (First Line of Defense)

Every external call has an explicit timeout. Never use defaults.

```python
# BAD: No timeout - a slow dependency blocks your thread forever
response = requests.get("https://payment-service/charge")

# BAD: Timeout too generous - 30 seconds of blocked threads = cascading failure
response = requests.get("https://payment-service/charge", timeout=30)

# GOOD: Aggressive timeout with connect and read separated
response = requests.get(
    "https://payment-service/charge",
    timeout=(1.0, 5.0),  # 1s connect, 5s read
)
```

Timeout rules:

| Dependency Type | Connect Timeout | Read Timeout | Rationale |
|----------------|----------------|--------------|-----------|
| Internal service (same region) | 1s | 5s | Should be fast; detect failures quickly |
| Internal service (cross-region) | 2s | 10s | Network latency is higher |
| Database (primary) | 1s | 3s | DB calls should be fast; slow = problem |
| Cache (Redis/Memcached) | 500ms | 1s | Cache misses should be fast |
| External third-party API | 2s | 15s | Less control, but still bound it |
| Non-critical dependency | 500ms | 2s | Fail fast, degrade gracefully |

### 2. Retries with Exponential Backoff and Jitter

Retries are essential but dangerous. Without backoff, retries amplify load on a struggling service:

```python
from tenacity import retry, stop_after_attempt, wait_exponential_jitter

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential_jitter(
        initial=0.1,      # First retry after ~100ms
        max=10,           # Never wait more than 10s
        jitter=2,         # Add random jitter up to 2s
    ),
    retry=retry_if_exception_type((TransientError, TimeoutError)),
)
def call_payment_service(order_id: str) -> PaymentResult:
    return payment_client.charge(order_id)
```

Retry rules:
- **Only retry transient errors** — never retry 400s, auth failures, or validation errors
- **Exponential backoff** — 100ms → 200ms → 400ms (not 100ms → 100ms → 100ms)
- **Full jitter** — randomize wait time to prevent thundering herd
- **Limited attempts** — 3 attempts maximum for synchronous paths
- **Budget-based retries** — limit total retries per time window (e.g., 10% of traffic can be retries)

```python
class RetryBudget:
    """Limits retries to a percentage of total requests."""

    def __init__(self, budget_percent: float = 10.0, window_seconds: int = 60):
        self.budget_percent = budget_percent
        self.window_seconds = window_seconds
        self._total_requests = 0
        self._retry_requests = 0

    def can_retry(self) -> bool:
        if self._total_requests == 0:
            return True
        retry_rate = (self._retry_requests / self._total_requests) * 100
        return retry_rate < self.budget_percent
```

### 3. Circuit Breakers

Circuit breakers prevent calling a known-failing dependency:

```python
from circuitbreaker import CircuitBreaker

payment_circuit = CircuitBreaker(
    failure_threshold=5,       # Open after 5 consecutive failures
    recovery_timeout=30,       # Try again after 30 seconds
    expected_exception=(TransientError, TimeoutError),
)

@payment_circuit
def call_payment_service(order_id: str) -> PaymentResult:
    return payment_client.charge(order_id)


def process_payment(order_id: str) -> PaymentResult:
    try:
        return call_payment_service(order_id)
    except CircuitBreakerError:
        # Circuit is open - dependency is known-bad
        logger.warning("payment.circuit_open", order_id=order_id)
        metrics.count("PaymentCircuit.Open", 1)
        raise PaymentUnavailableError("Payment service temporarily unavailable")
```

Circuit breaker states:

```
┌──────────┐     failures >= threshold     ┌──────────┐
│  CLOSED  │ ─────────────────────────────→ │   OPEN   │
│(normal)  │                                │(failing) │
└──────────┘                                └──────────┘
     ↑                                           │
     │         success                           │ recovery_timeout elapsed
     │                                           ↓
     │                                    ┌────────────┐
     └─────────────────────────────────── │ HALF-OPEN  │
                                          │(testing)   │
                                          └────────────┘
```

Circuit breaker metrics to emit:
- `CircuitBreaker.StateChange` (with from/to dimensions)
- `CircuitBreaker.Rejected` (requests rejected while open)
- `CircuitBreaker.HalfOpenSuccess` / `CircuitBreaker.HalfOpenFailure`

### 4. Bulkhead Pattern

Bulkheads isolate dependency failures so one bad dependency doesn't consume all resources:

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

class BulkheadedDependencies:
    """Each dependency gets its own thread pool - one failing dependency
    can't starve others of threads."""

    def __init__(self):
        # Payment gets 10 threads - if it's slow, only these 10 block
        self.payment_pool = ThreadPoolExecutor(
            max_workers=10, thread_name_prefix="payment"
        )
        # Inventory gets 20 threads - higher traffic, isolated from payment
        self.inventory_pool = ThreadPoolExecutor(
            max_workers=20, thread_name_prefix="inventory"
        )
        # Recommendations is non-critical - only 5 threads
        self.recommendations_pool = ThreadPoolExecutor(
            max_workers=5, thread_name_prefix="recommendations"
        )

    async def get_payment_status(self, order_id: str):
        return await asyncio.get_event_loop().run_in_executor(
            self.payment_pool,
            payment_client.get_status,
            order_id,
        )
```

Bulkhead strategies:

| Strategy | Use When | Implementation |
|----------|---------|---------------|
| Thread pool isolation | Blocking I/O calls | Separate ThreadPoolExecutor per dependency |
| Semaphore isolation | Async calls | asyncio.Semaphore limiting concurrent calls |
| Connection pool isolation | Database connections | Separate connection pools per use case |
| Queue isolation | Message processing | Separate queues for different priority levels |

### 5. Graceful Degradation Strategy

Classify every dependency as critical or non-critical:

```python
class DependencyClassification:
    """
    CRITICAL: Failure means we cannot serve the customer at all.
              Example: Database for order data, Auth service
              Strategy: Retry, circuit break, return error to caller

    NON-CRITICAL: Failure means reduced functionality but core works.
                  Example: Recommendations, analytics, personalization
                  Strategy: Timeout aggressively, return default, log and continue
    """
    pass


def get_product_page(product_id: str) -> ProductPage:
    # CRITICAL: Product data - no fallback possible
    product = product_service.get(product_id)  # Full retry + circuit breaker

    # NON-CRITICAL: Reviews - show page without reviews if unavailable
    try:
        reviews = review_service.get_reviews(
            product_id, timeout_ms=200
        )
    except (TimeoutError, ServiceError):
        metrics.count("Reviews.Degraded", 1)
        reviews = CachedReviews.get(product_id, default=[])

    # NON-CRITICAL: Recommendations - show page without recs
    try:
        recommendations = rec_service.get_similar(
            product_id, timeout_ms=150
        )
    except (TimeoutError, ServiceError):
        metrics.count("Recommendations.Degraded", 1)
        recommendations = []

    return ProductPage(
        product=product,
        reviews=reviews,
        recommendations=recommendations,
    )
```

### 6. Dependency Isolation Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     Your Service                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────────┐  ┌──────────────────┐            │
│  │  Payment Client   │  │ Inventory Client  │           │
│  │  ┌─────────────┐ │  │  ┌─────────────┐ │           │
│  │  │  Timeout     │ │  │  │  Timeout     │ │           │
│  │  │  Retry       │ │  │  │  Retry       │ │           │
│  │  │  Circuit Brk │ │  │  │  Circuit Brk │ │           │
│  │  │  Bulkhead    │ │  │  │  Bulkhead    │ │           │
│  │  │  Metrics     │ │  │  │  Metrics     │ │           │
│  │  └─────────────┘ │  │  └─────────────┘ │           │
│  └──────────────────┘  └──────────────────┘            │
│                                                         │
│  ┌──────────────────┐  ┌──────────────────┐            │
│  │  Cache Client     │  │  Recs Client     │           │
│  │  (non-critical)   │  │  (non-critical)  │           │
│  │  ┌─────────────┐ │  │  ┌─────────────┐ │           │
│  │  │  Timeout(1s) │ │  │  │ Timeout(200ms)│ │          │
│  │  │  No retry    │ │  │  │  No retry    │ │           │
│  │  │  Fallback    │ │  │  │  Fallback:[] │ │           │
│  │  │  Metrics     │ │  │  │  Metrics     │ │           │
│  │  └─────────────┘ │  │  └─────────────┘ │           │
│  └──────────────────┘  └──────────────────┘            │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 7. Dependency Client Template

```python
class ResilientServiceClient:
    """Template for a properly-managed dependency client."""

    def __init__(self, config: ClientConfig):
        self.config = config
        self.circuit_breaker = CircuitBreaker(
            failure_threshold=config.circuit_failure_threshold,
            recovery_timeout=config.circuit_recovery_seconds,
        )
        self.retry_budget = RetryBudget(
            budget_percent=config.retry_budget_percent,
        )
        self.metrics = MetricsClient(namespace=config.service_name)
        self.logger = structlog.get_logger(dependency=config.service_name)

    def call(self, operation: str, request: dict) -> dict:
        self.metrics.count(f"{operation}.Attempt", 1)

        try:
            with self.metrics.timer(f"{operation}.Latency"):
                response = self._execute_with_resilience(operation, request)
            self.metrics.count(f"{operation}.Success", 1)
            return response

        except CircuitBreakerError:
            self.metrics.count(f"{operation}.CircuitOpen", 1)
            self.logger.warning(f"{operation}.circuit_open")
            raise DependencyUnavailableError(self.config.service_name)

        except TimeoutError:
            self.metrics.count(f"{operation}.Timeout", 1)
            self.logger.warning(f"{operation}.timeout", timeout_ms=self.config.read_timeout_ms)
            raise

        except Exception as e:
            self.metrics.count(f"{operation}.Error", 1)
            self.logger.error(f"{operation}.failed", error=str(e))
            raise

    @circuit_breaker
    @retry_with_backoff
    def _execute_with_resilience(self, operation: str, request: dict) -> dict:
        return self.http_client.post(
            url=f"{self.config.base_url}/{operation}",
            json=request,
            timeout=(self.config.connect_timeout_ms / 1000, self.config.read_timeout_ms / 1000),
        )
```

## Mechanisms Over Good Intentions

| Mechanism | What It Enforces | How |
|-----------|-----------------|-----|
| Mandatory timeout configuration | No unbounded calls | Client library requires timeout parameter (no default) |
| Circuit breaker metrics in dashboard | Visibility into dependency health | ORR requires dependency health dashboard |
| Chaos engineering (GameDays) | Resilience actually works | Quarterly failure injection verifies degradation paths |
| Dependency scorecard | Explicit classification | Every dependency documented as critical/non-critical with SLO |
| Load testing with dependency failures | Verify graceful degradation | Pre-launch load test includes dependency failure scenarios |

## Common Rationalizations

| Rationalization | Why It's Wrong | What To Do Instead |
|----------------|----------------|-------------------|
| "That service has 99.99% availability, we don't need a circuit breaker" | 99.99% means 52 minutes of downtime per year. When those 52 minutes happen during your peak traffic, your service goes down too. | Add the circuit breaker. The cost is a few dozen lines of code. The savings is avoiding a cascading outage. |
| "Retries will handle transient errors" | Retries without backoff and jitter turn a hiccup into a thundering herd. Your retries become the DDoS that kills the dependency. | Always exponential backoff. Always full jitter. Always a retry budget. Always stop retrying when the circuit opens. |
| "We'll add timeouts when we see slow responses" | By the time you see slow responses, your thread pool is exhausted and your service is down. Timeouts prevent the damage. | Set timeouts from day one. Start aggressive (1-2s). Loosen only with data showing you need more. |
| "The bulkhead pattern is over-engineering" | One slow dependency consuming all your threads is not theoretical—it's Amazon's most common cascading failure pattern. | If you have more than 2 external dependencies, you need bulkheads. Period. The cost is configuration. The savings is availability. |
| "We cache everything so we don't really depend on that service" | Caches expire. Cache invalidation bugs happen. Cold starts have empty caches. Your "cached" dependency is still a dependency. | Cache improves performance but doesn't eliminate the dependency. Still add timeouts, circuit breakers, and fallbacks for cache misses. |

## Red Flags

- HTTP calls without explicit timeouts
- Retries without exponential backoff or jitter
- No circuit breakers on any external service call
- All dependencies share one thread/connection pool
- No distinction between critical and non-critical dependencies
- Retry loops that retry all errors (including 400s and auth failures)
- Service goes down when a non-critical dependency is unavailable
- No metrics on dependency latency or error rates
- Default timeout values (30s, 60s) that nobody has reviewed
- Load tests don't include dependency failure scenarios

## Verification

After implementing dependency management, verify:

- [ ] Every external call has an explicit, reviewed timeout
- [ ] Retries use exponential backoff with full jitter
- [ ] Retry budget limits total retry volume
- [ ] Circuit breakers exist on all critical dependency calls
- [ ] Bulkheads isolate dependencies into separate resource pools
- [ ] Non-critical dependencies degrade gracefully (not crash)
- [ ] Dependency health is visible on the service dashboard
- [ ] GameDay/chaos testing has verified degradation paths work
- [ ] Dependency SLOs are documented and alarmed
- [ ] Fallback values are tested and correct

## Tenets

1. **Every dependency will fail.** Not might. Will. Design for the failure case first, the happy path second.
2. **Timeouts are mandatory.** An unbounded call is a thread leak waiting to happen. Explicit timeouts on every network call. No exceptions.
3. **Retries are amplifiers.** Without backoff and budget, retries make outages worse. A retry storm is a self-inflicted DDoS.
4. **Circuit breakers are kindness.** They protect you from a failing dependency and protect the failing dependency from your retry traffic. Both benefit.
5. **Isolate blast radius.** One failing dependency should not consume the resources needed for other dependencies. Bulkheads exist for this reason.
6. **Degrade, don't fail.** If you can serve 80% of the response without a non-critical dependency, serve 80%. The customer would rather see something than an error page.
7. **Verify with chaos.** Resilience patterns that are never tested are hope-based engineering. Inject failures regularly. Fix what breaks.
