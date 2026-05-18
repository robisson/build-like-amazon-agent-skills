---
name: Test-Driven Development
description: Red-Green-Refactor cycle with Amazon's test pyramid (80% unit, 15% integration, 5% e2e). Coverage gates, DAMP over DRY in tests, canary tests in production.
leadership_principles:
  - Insist on the Highest Standards
  - Ownership
  - Dive Deep
---

## Overview

Test-Driven Development (TDD) at Amazon means writing the test before the implementation—always. The Red-Green-Refactor cycle is not a suggestion; it is the mechanism that ensures code correctness, enables fearless refactoring, and keeps deployment pipelines green.

Amazon's test philosophy follows the test pyramid: a broad base of fast unit tests (80%), a middle layer of integration tests (15%), and a thin cap of end-to-end tests (5%). This ratio exists because unit tests are fast, deterministic, and cheap to maintain. Integration tests verify contracts between components. End-to-end tests validate customer-visible behavior but are slow and brittle.

Beyond pre-deployment testing, Amazon runs canary tests in production—synthetic requests that continuously verify real system behavior. When canaries fail, alarms fire before customers notice.

## When to Use

- Before writing any production code (the "Red" step comes first)
- When fixing a bug (write the failing test that reproduces it first)
- When refactoring existing code (ensure tests exist before changing behavior)
- During code review (verify test coverage for every behavior change)
- When setting up deployment pipelines (configure coverage gates)
- When onboarding a new service (establish canary tests immediately)

## Amazon Context

At Amazon, untested code does not ship. Pipelines enforce minimum coverage thresholds (typically 80% line coverage, 90% branch coverage for critical paths). Code review explicitly evaluates test quality—a change without tests is rejected regardless of how correct the implementation appears.

The Builder Tools ecosystem (Brazil, CDK Pipelines, CodeGuru) integrates testing at every stage: pre-commit hooks run unit tests locally, CI runs the full suite, and post-deployment canaries verify production health. Teams own their test infrastructure the same way they own their production infrastructure.

Amazon's testing culture learned from expensive failures: services that shipped with "we'll add tests later" invariably accumulated tech debt that made changes risky, deployments scary, and on-call rotations miserable. TDD inverts this—tests are the first thing you build, not the last.

## The Process

### 1. Red-Green-Refactor Cycle

```
┌─────────────────────────────────────────┐
│  RED: Write a failing test              │
│  ↓                                       │
│  GREEN: Write minimum code to pass      │
│  ↓                                       │
│  REFACTOR: Clean up, tests still pass   │
│  ↓                                       │
│  Repeat                                  │
└─────────────────────────────────────────┘
```

**Red Phase:**
- Write one test that describes desired behavior
- Run it. It must fail. If it passes, your test is wrong.
- The test name describes the behavior: `test_order_rejected_when_inventory_zero`

**Green Phase:**
- Write the minimum code to make the test pass
- No premature abstraction. No "while I'm here" changes.
- Hardcode values if that's all the test requires—the next test will force generalization.

**Refactor Phase:**
- Now clean up both production and test code
- Extract methods, rename variables, remove duplication
- Run tests after every change. All must stay green.

### 2. Test Pyramid

| Layer | Percentage | Scope | Speed | Characteristics |
|-------|-----------|-------|-------|----------------|
| Unit | 80% | Single class/function | < 10ms each | No I/O, no network, no database. Mocked dependencies. |
| Integration | 15% | Component boundaries | < 5s each | Real database (local), real HTTP calls (to test containers). |
| End-to-End | 5% | Full customer journey | < 60s each | Real infrastructure. Fragile. Few but critical. |

### 3. Writing Effective Unit Tests (DAMP over DRY)

DAMP = Descriptive And Meaningful Phrases. In tests, clarity beats brevity.

```python
# BAD: DRY but unreadable
def test_order(self):
    order = self._make_order(status=3, items=2)
    self.assertEqual(order.total, self._expected(2))

# GOOD: DAMP - each test tells a complete story
def test_order_total_sums_item_prices_with_tax(self):
    order = Order(
        items=[
            OrderItem(name="Widget", price=Money(10, "USD")),
            OrderItem(name="Gadget", price=Money(20, "USD")),
        ],
        tax_rate=Decimal("0.08"),
    )

    total = order.calculate_total()

    assert total == Money(32.40, "USD")  # (10 + 20) * 1.08
```

DAMP principles:
- **Arrange-Act-Assert** structure in every test (visible sections)
- **No shared setup that hides context** — if a test needs data, show it in the test
- **Test names are documentation** — `test_<behavior>_when_<condition>_then_<outcome>`
- **One assertion per test** (one logical assertion; multiple `assert` calls for one concept is fine)
- **Helper factories over fixtures** — `make_order(status="pending")` beats `self.order`

### 4. Coverage Gates

Configure in CI/CD pipeline:

```yaml
coverage:
  minimum:
    line: 80
    branch: 80
  critical_paths:
    line: 95
    branch: 90
  fail_on_decrease: true
  exclude:
    - "*/generated/*"
    - "*/migrations/*"
```

Rules:
- Coverage can never decrease on a PR (ratchet mechanism)
- Critical paths (payment, auth, data integrity) require 95%+
- New files must have 90%+ coverage or PR is blocked
- Coverage is measured on production code only (not test code)

### 5. Test Categories and Tagging

```python
@pytest.mark.unit
def test_calculate_shipping_cost():
    ...

@pytest.mark.integration
def test_order_persisted_to_dynamodb():
    ...

@pytest.mark.e2e
def test_customer_can_complete_checkout():
    ...

@pytest.mark.canary
def test_homepage_loads_under_2_seconds():
    ...
```

Execution contexts:
- **Pre-commit**: Unit tests only (< 30 seconds total)
- **CI pipeline**: Unit + Integration (< 10 minutes total)
- **Pre-deployment**: Unit + Integration + E2E (< 30 minutes)
- **Production**: Canary tests (continuous, every 1-5 minutes)

### 6. Canary Tests in Production

Canary tests are synthetic requests that exercise real production infrastructure:

```python
class OrderServiceCanary:
    """Runs every 60 seconds against production."""

    def test_create_order_happy_path(self):
        """Place a test order and verify it appears in the system."""
        order = self.client.create_order(
            customer_id=CANARY_CUSTOMER_ID,
            items=[CANARY_ITEM],
            idempotency_key=f"canary-{uuid4()}",
        )
        assert order.status == "PLACED"
        assert order.id is not None

        # Verify read-after-write
        retrieved = self.client.get_order(order.id)
        assert retrieved.status == "PLACED"

        # Cleanup
        self.client.cancel_order(order.id, reason="CANARY_TEST")

    def test_order_service_latency(self):
        """Verify p99 latency is under SLA."""
        start = time.monotonic()
        self.client.get_order(KNOWN_ORDER_ID)
        latency_ms = (time.monotonic() - start) * 1000
        assert latency_ms < 500, f"Latency {latency_ms}ms exceeds 500ms SLA"
```

Canary rules:
- Use dedicated canary accounts/data (never real customer data)
- Clean up after themselves (no test data accumulation)
- Alert on failure within 5 minutes (high-severity alarm)
- Cover critical customer journeys (top 3-5 paths)
- Run in every region independently

### 7. Test Quality Checklist

For every PR, verify tests meet the bar:

- [ ] Tests fail for the right reason (verified during Red phase)
- [ ] Tests are independent (can run in any order)
- [ ] Tests are deterministic (no flaky timing dependencies)
- [ ] Tests are fast (unit < 10ms, integration < 5s)
- [ ] Test names describe behavior, not implementation
- [ ] No logic in tests (no `if`, no loops, no try/catch)
- [ ] Mocks verify interactions, not implementation details
- [ ] Boundary conditions tested (empty, null, max, overflow)
- [ ] Error paths tested (exceptions, timeouts, invalid input)

## Mechanisms Over Good Intentions

| Mechanism | What It Enforces | How |
|-----------|-----------------|-----|
| Coverage gates in CI | Minimum test coverage | PR blocked if coverage below threshold or decreases |
| Pre-commit test hooks | Tests run before push | Git hook executes unit tests; push rejected on failure |
| Canary alarm escalation | Production health | PagerDuty alert if canary fails 3 consecutive times |
| Test-to-code ratio metric | Sufficient test investment | Dashboard tracks ratio; reviewed in sprint retrospective |
| Mutation testing (periodic) | Test effectiveness | Monthly mutation run; low mutation kill rate triggers action |

## Common Rationalizations

| Rationalization | Why It's Wrong | What To Do Instead |
|----------------|----------------|-------------------|
| "I'll add tests after the implementation is stable" | Code without tests is never stable. It's unknown. You'll ship bugs, then write tests around the bugs, cementing them as "expected behavior." | Write the test first. Always. The test defines what "stable" means. |
| "This code is too simple to test" | Simple code becomes complex code. When it does, you'll be afraid to change it. Getters today become business logic tomorrow. | Test the behavior, not the complexity. Simple tests for simple code are fast to write and valuable as documentation. |
| "Mocking makes tests brittle" | Over-mocking makes tests brittle. Strategic mocking at boundaries enables fast, deterministic tests. | Mock at architectural boundaries (database, network, clock). Don't mock internal collaborators—test them together. |
| "100% coverage is our goal" | Coverage measures lines executed, not correctness. 100% coverage with no assertions is useless. Quality over quantity. | Target meaningful coverage: 80% overall, 95% for critical paths. Focus on branch coverage and mutation testing for quality. |
| "End-to-end tests give more confidence" | E2E tests are slow, flaky, and expensive. A failing E2E test tells you something broke but not what. They create false confidence. | Invest in the pyramid. Strong unit tests + focused integration tests give better fault isolation than E2E suites. |

## Red Flags

- PR has production code changes but no new or modified tests
- Test suite takes more than 10 minutes to run locally
- Tests break when implementation details change (over-mocking)
- Flaky tests are "retried until green" instead of fixed
- Test names are `test1`, `test2`, `testHelper` (meaningless)
- Tests have complex setup shared across unrelated tests
- Coverage is high but bugs still escape to production (assertion-free tests)
- No canary tests exist for a production service
- Team says "we'll write tests during the hardening sprint"

## Verification

After implementing with TDD, verify:

- [ ] Every public behavior has at least one test (preferably written first)
- [ ] Test pyramid ratios are approximately correct (80/15/5)
- [ ] Coverage gates are configured and enforced in CI
- [ ] All tests are deterministic (run suite 3x, same results)
- [ ] Canary tests are running in production and alarming on failure
- [ ] Test suite runs in under 10 minutes in CI
- [ ] Mutation testing kill rate is above 70%
- [ ] New team members can understand behavior from test names alone
- [ ] No test relies on test execution order

## Tenets

1. **Red before Green.** Never write production code without a failing test. The test defines the requirement. No test = no requirement = no code.
2. **Tests are production code.** They deserve the same quality, review, and maintenance attention. Sloppy tests create sloppy confidence.
3. **Fast feedback above all.** A test that takes 10 seconds to tell you something is broken is 1000x more valuable than a test that takes 10 minutes.
4. **DAMP over DRY in tests.** Readability and independence matter more than avoiding duplication. Each test is a specification—it should be self-contained.
5. **Test behavior, not implementation.** Tests should survive refactoring. If renaming a private method breaks tests, you're testing the wrong thing.
6. **Canaries never sleep.** Production testing is not optional. If you can't verify your service works right now, you don't know if it works right now.
7. **Fix flaky tests immediately.** A flaky test is worse than no test—it trains the team to ignore failures. Delete it or fix it. Today.
