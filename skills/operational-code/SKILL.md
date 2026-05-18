---
name: Operational Code
description: Writing code with built-in observability from day one. Structured logging (JSON), metrics emission (latency p50/p99, error rates), alarm-ready code, request tracing, graceful degradation.
leadership_principles:
  - Ownership
  - Insist on the Highest Standards
  - Dive Deep
---

## Overview

Operational code is production code that tells you how it's doing without anyone asking. Every function emits metrics, every request leaves a trace, every error provides context. At Amazon, "it works on my machine" is meaningless—what matters is whether it works in production right now, under load, at 3 AM.

Writing operational code means embedding observability into the implementation from the first line. Not as an afterthought, not as a "hardening sprint" task—from the start. When an alarm fires, operational code gives you the dashboard, the log query, and the trace ID to diagnose the issue in minutes, not hours.

The principle is simple: if you can't observe it, you can't operate it. If you can't operate it, you shouldn't ship it.

## When to Use

- Writing any production code (this is not optional)
- Implementing new API endpoints or message handlers
- Adding external service calls or database queries
- Handling errors, retries, or fallback paths
- Implementing feature flags or configuration changes
- Building background jobs, queues, or async workflows

## Amazon Context

Amazon operates thousands of services at massive scale. When something goes wrong, the operator (often the developer who wrote the code, on-call at 2 AM) needs to answer three questions in under 5 minutes:

1. **What is broken?** (Metrics and alarms tell you)
2. **Since when?** (Dashboards with time correlation tell you)
3. **Why?** (Structured logs and traces tell you)

Services that don't emit proper telemetry become operational black holes—they break, nobody knows why, and recovery takes hours of guessing. Amazon's operational bar requires that every service ships with dashboards, alarms, and runbooks before launch (enforced through ORR—Operational Readiness Review).

CloudWatch, X-Ray, and internal tooling provide the infrastructure. But the instrumentation must live in the code. No external tool can observe what the code doesn't emit.

## The Process

### 1. Structured Logging (JSON)

Every log statement is a JSON object with consistent fields:

```python
import structlog

logger = structlog.get_logger()

def process_order(order_id: str, customer_id: str) -> Order:
    logger.info(
        "order.processing.started",
        order_id=order_id,
        customer_id=customer_id,
        item_count=len(order.items),
    )

    try:
        result = payment_service.charge(order.total)
        logger.info(
            "order.payment.succeeded",
            order_id=order_id,
            payment_id=result.payment_id,
            amount_cents=order.total.cents,
            latency_ms=result.latency_ms,
        )
    except PaymentDeclinedError as e:
        logger.warning(
            "order.payment.declined",
            order_id=order_id,
            decline_reason=e.reason,
            card_last_four=e.card_last_four,
        )
        raise
    except Exception as e:
        logger.error(
            "order.payment.failed",
            order_id=order_id,
            error_type=type(e).__name__,
            error_message=str(e),
            exc_info=True,
        )
        raise
```

Structured logging rules:
- **Always JSON** — never free-form strings. Machines parse logs, not humans.
- **Event name as first argument** — dot-separated, hierarchical: `service.component.action`
- **Include identifiers** — request_id, order_id, customer_id for correlation
- **Include measurements** — latency_ms, item_count, retry_attempt for diagnostics
- **Log levels are semantic** — INFO for business events, WARNING for recoverable issues, ERROR for failures requiring attention
- **Never log secrets** — no passwords, tokens, full credit card numbers, PII

### 2. Metrics Emission

Every operation emits latency, count, and error metrics:

```python
from metrics import MetricsClient

metrics = MetricsClient(namespace="OrderService")

def process_order(order_id: str) -> Order:
    with metrics.timer("ProcessOrder.Latency"):
        try:
            result = _do_process_order(order_id)
            metrics.count("ProcessOrder.Success", 1)
            return result
        except ValidationError:
            metrics.count("ProcessOrder.ValidationError", 1)
            raise
        except PaymentError:
            metrics.count("ProcessOrder.PaymentError", 1)
            raise
        except Exception:
            metrics.count("ProcessOrder.UnexpectedError", 1)
            raise
```

Standard metrics for every operation:

| Metric | Type | Dimensions | Alarm Threshold |
|--------|------|-----------|----------------|
| `{Operation}.Latency` | Timer (p50, p90, p99) | Operation, Region | p99 > 2x baseline |
| `{Operation}.Success` | Count | Operation, Region | Rate < 99.9% |
| `{Operation}.Error` | Count | Operation, ErrorType | Rate > 0.1% |
| `{Operation}.Throttle` | Count | Operation, Region | Any occurrence |
| `{Operation}.Fault` | Count (5xx) | Operation, Region | Rate > 0.01% |
| `{Dependency}.Latency` | Timer | Dependency, Operation | p99 > SLA |
| `{Dependency}.Error` | Count | Dependency, ErrorType | Rate > 1% |

### 3. Request Tracing

Every request gets a trace ID that propagates across service boundaries:

```python
from tracing import Tracer

tracer = Tracer(service_name="OrderService")

@tracer.capture_method
def process_order(order_id: str) -> Order:
    # Trace ID automatically propagated to downstream calls
    with tracer.subsegment("validate_order"):
        validate(order_id)

    with tracer.subsegment("charge_payment"):
        payment_service.charge(order.total)  # Trace ID in header

    with tracer.subsegment("persist_order"):
        order_repo.save(order)  # Trace ID in metadata
```

Tracing rules:
- **Every inbound request gets a trace ID** (generated or propagated from caller)
- **Trace ID appears in every log line** (for correlation)
- **Trace ID propagates to all downstream calls** (HTTP headers, message attributes)
- **Subsegments wrap every I/O operation** (database, cache, service calls)
- **Annotations mark business-relevant data** (customer_tier, order_type) for filtering

### 4. Alarm-Ready Code

Code is written so that alarming is trivial—metrics are already emitted at the right granularity:

```python
# Alarm definition (CloudWatch / infrastructure-as-code)
alarms:
  - name: OrderService-HighErrorRate
    metric: ProcessOrder.Error
    threshold: 10  # errors per minute
    period: 60
    evaluation_periods: 3  # 3 consecutive minutes
    comparison: GreaterThanThreshold
    actions: [page-oncall]

  - name: OrderService-HighLatency
    metric: ProcessOrder.Latency
    statistic: p99
    threshold: 2000  # milliseconds
    period: 300  # 5 minutes
    evaluation_periods: 2
    comparison: GreaterThanThreshold
    actions: [page-oncall]

  - name: OrderService-DependencyDegraded
    metric: PaymentService.Error
    threshold: 5
    period: 60
    evaluation_periods: 2
    actions: [notify-team]
```

Alarm philosophy:
- **Alarm on symptoms, not causes** — high latency, not high CPU
- **Every alarm has a runbook link** — the alarm description contains the URL
- **Every alarm is actionable** — if you can't act on it, it's noise. Remove it.
- **Alarms have severity levels** — P2 (High) pages on-call, P4 (Low) notifies Slack
- **Test your alarms** — deliberately inject failures to verify alarms fire

### 5. Graceful Degradation

Operational code fails gracefully—it never takes down the whole system for a partial failure:

```python
def get_order_with_recommendations(order_id: str) -> OrderResponse:
    # Critical path: must succeed
    order = order_service.get_order(order_id)

    # Non-critical: degrade gracefully
    try:
        recommendations = recommendation_service.get_for_order(
            order_id, timeout_ms=200
        )
    except (TimeoutError, ServiceUnavailableError) as e:
        logger.warning(
            "recommendations.degraded",
            order_id=order_id,
            error_type=type(e).__name__,
        )
        metrics.count("Recommendations.Degraded", 1)
        recommendations = []  # Safe default: empty recommendations

    return OrderResponse(order=order, recommendations=recommendations)
```

Degradation principles:
- **Distinguish critical from non-critical dependencies** — document which failures are acceptable
- **Always have a fallback** — cached data, empty response, default value
- **Emit metrics on degradation** — you need to know when you're running degraded
- **Set aggressive timeouts on non-critical paths** — 200ms, not 30 seconds
- **Never let a non-critical failure become a critical failure** — isolate blast radius

### 6. Operational Code Template

Every new handler/endpoint follows this template:

```python
@tracer.capture_method
def handler(event: Event) -> Response:
    """
    Metrics emitted:
      - Handler.Latency (timer)
      - Handler.Success / Handler.Error (counter)
      - Handler.InputValidationError (counter)
    Alarms:
      - Handler-HighErrorRate (> 5/min for 3 min → page)
      - Handler-HighLatency (p99 > 1s for 5 min → page)
    Logs:
      - handler.started (INFO)
      - handler.succeeded (INFO)
      - handler.failed (ERROR)
    """
    request_id = event.request_id or str(uuid4())

    logger.info("handler.started", request_id=request_id, input_size=len(event.body))

    with metrics.timer("Handler.Latency"):
        try:
            # Validate
            validated_input = validate(event.body)

            # Execute
            result = execute_business_logic(validated_input)

            # Respond
            metrics.count("Handler.Success", 1)
            logger.info("handler.succeeded", request_id=request_id, result_id=result.id)
            return Response(status=200, body=result)

        except ValidationError as e:
            metrics.count("Handler.InputValidationError", 1)
            logger.warning("handler.validation_failed", request_id=request_id, field=e.field)
            return Response(status=400, body={"error": str(e)})

        except Exception as e:
            metrics.count("Handler.Error", 1)
            logger.error("handler.failed", request_id=request_id, error=str(e), exc_info=True)
            return Response(status=500, body={"error": "Internal error", "request_id": request_id})
```

## Mechanisms Over Good Intentions

| Mechanism | What It Enforces | How |
|-----------|-----------------|-----|
| Metric coverage in PR review | Every code path emits telemetry | Code Review checklist item: "Are metrics and logs adequate?" |
| Alarm-per-dashboard rule | Every dashboard has corresponding alarms | ORR verifies alarm existence for each metric |
| Structured log linting | JSON format with required fields | CI linter rejects free-form log.info("something happened") |
| Trace propagation tests | Trace IDs flow across boundaries | Integration tests assert trace header presence |
| Operational readiness review | Full observability before launch | Service blocked from prod without passing ORR |

## Common Rationalizations

| Rationalization | Why It's Wrong | What To Do Instead |
|----------------|----------------|-------------------|
| "We'll add observability after launch" | After launch = after the first incident you can't diagnose. You'll add it in a panic, poorly, under pressure. | Observability is a launch blocker. No dashboard + no alarms = no launch. Enforce via ORR. |
| "Logging everything will be expensive" | Logging nothing is more expensive—the first undiagnosable incident costs more than a year of CloudWatch bills. | Log at appropriate levels. INFO for business events, DEBUG for details (disabled in prod unless needed). Use sampling for high-volume paths. |
| "Metrics add latency to the hot path" | Metric emission is async and non-blocking. The latency is negligible (< 1μs per metric point). | Use async metric publishing. Batch emissions. The overhead is unmeasurable compared to any I/O operation. |
| "The traces are too noisy to be useful" | Noisy traces mean your instrumentation granularity is wrong, not that tracing is wrong. | Add subsegments at architectural boundaries only. Annotate with business context. Filter by trace annotations when investigating. |
| "We have logs, we don't need metrics" | Logs tell you what happened to one request. Metrics tell you what's happening to all requests. You need both. | Metrics for detection (is something wrong?), logs for diagnosis (what specifically is wrong?), traces for correlation (where in the chain did it break?). |

## Red Flags

- A service has no dashboard or the dashboard has no data
- Alarms exist but nobody has been paged by them (untested)
- Logs use `print()` or unstructured `logger.info(f"Processing {x}")`
- No trace IDs appear in log statements
- Error handling swallows exceptions with empty `except: pass`
- Metrics exist but no alarms are configured against them
- A new endpoint ships without latency and error metrics
- On-call engineer says "I don't know how to tell if this service is healthy"
- Fallback paths have no metrics (you can't tell when you're degraded)

## Verification

After writing operational code, verify:

- [ ] Every API endpoint emits latency (p50/p99) and error rate metrics
- [ ] Every external dependency call has its own latency and error metrics
- [ ] All logs are structured JSON with trace_id, request_id, and timestamp
- [ ] Alarms exist for every critical metric with documented thresholds
- [ ] Every alarm links to a runbook with diagnosis and remediation steps
- [ ] Trace IDs propagate from ingress to all downstream calls
- [ ] Graceful degradation is implemented for non-critical dependencies
- [ ] A dashboard exists showing service health at a glance
- [ ] Synthetic canaries verify production health continuously
- [ ] Team can answer "is the service healthy right now?" in under 30 seconds

## Tenets

1. **Observable by default.** If you write a function that does I/O, it emits metrics and logs. This is not negotiable. Unobservable code is unoperatable code.
2. **Metrics for detection, logs for diagnosis, traces for correlation.** Each telemetry type serves a distinct purpose. You need all three.
3. **Alarms are promises to customers.** Every alarm says "we will notice before you do." An alarm that fires and is ignored is a broken promise.
4. **Structured or nothing.** Free-form logs are grep fodder. Structured logs are queryable, aggregatable, and dashboardable. Always JSON. Always consistent fields.
5. **Degrade, never crash.** A non-critical dependency failure should result in reduced functionality, not a 500 error. Know which dependencies are critical.
6. **The on-call test.** Before merging, ask: "If this breaks at 3 AM, can the on-call engineer diagnose and fix it with what I've instrumented?" If no, add more observability.
7. **Emit early, emit often.** It's cheap to emit a metric you never look at. It's expensive to wish you had a metric during an incident.
