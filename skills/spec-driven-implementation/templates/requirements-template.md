# Requirements: [Slice Name]

> **Spec for**: [Parent Design Document title and link]
> **Slice**: [N of M] — [One-line description of what this slice delivers]
> **Author**: [Name]
> **Status**: Draft | In Review | Approved
> **Last Updated**: [Date]

---

## 1. Introduction

### 1.1 Context

[Describe the broader system context. What exists today? What problem does this slice address? Reference the approved Design Document and explain which portion this spec covers.]

### 1.2 Scope

**In Scope:**
- [Specific capability or behavior this slice delivers]
- [Another specific deliverable]
- [Boundary: where this slice ends and the next begins]

**Non-Goals (explicitly out of scope for this slice):**
- [Feature or behavior deferred to a later slice]
- [Optimization that is not required in this iteration]
- [Integration that will be addressed in Slice N+1]

### 1.3 Design Document Reference

| Design Doc Section | Relevance to This Slice |
|-------------------|------------------------|
| §[N.N] [Section Title] | [How this section maps to this slice] |
| §[N.N] [Section Title] | [How this section maps to this slice] |

### 1.4 Assumptions

- [Assumption 1 — e.g., "The database schema from Slice 1 is deployed and stable"]
- [Assumption 2 — e.g., "Authentication service is available and returns JWT tokens"]
- [Assumption 3 — e.g., "Traffic will not exceed 1000 TPS during initial rollout"]

---

## 2. Glossary

| Term | Definition |
|------|-----------|
| [Term 1] | [Precise definition as used in this spec. Avoid "common knowledge" — define everything.] |
| [Term 2] | [Definition] |
| [Term 3] | [Definition] |

---

## 3. Requirements

### 3.1 [Feature Area 1]

#### Requirement 3.1.1: [Short Descriptive Name]

**User Story**: As a [specific role], I want [specific action] so that [measurable benefit].

**Acceptance Criteria**:

1. WHEN [user/system performs trigger action] the system SHALL [observable behavior with measurable outcome] — _Rationale: [why this matters]_
2. WHEN [trigger] AND [additional condition] the system SHALL [behavior] WITHIN [time bound] — _Rationale: [why this constraint]_
3. IF [error condition occurs] THEN the system MUST [recovery behavior] AND [notification behavior] — _Rationale: [why this recovery strategy]_
4. WHERE [deployment context / environment] the system SHALL [context-specific behavior] — _Rationale: [why context matters]_

**Priority**: P0 (launch blocker) | P1 (needed within 30 days) | P2 (future iteration)
**Design Ref**: §[section.number] of [Design Document Name]
**Verification**: [How this requirement will be tested — unit test, integration test, manual verification]

---

#### Requirement 3.1.2: [Short Descriptive Name]

**User Story**: As a [role], I want [action] so that [benefit].

**Acceptance Criteria**:

1. WHEN [trigger] the system SHALL [behavior] — _Rationale: [why]_
2. IF [condition] THEN the system MUST [behavior] — _Rationale: [why]_
3. the system SHALL NOT [prohibited behavior] UNDER ANY circumstances — _Rationale: [safety/security reason]_

**Priority**: P0 | P1 | P2
**Design Ref**: §[section.number]
**Verification**: [Test approach]

---

### 3.2 [Feature Area 2]

#### Requirement 3.2.1: [Short Descriptive Name]

**User Story**: As a [role], I want [action] so that [benefit].

**Acceptance Criteria**:

1. WHEN [trigger] the system SHALL [behavior] — _Rationale: [why]_
2. WHILE [ongoing condition] the system SHALL [continuous behavior] — _Rationale: [why]_
3. IF [boundary condition] THEN the system MUST [boundary handling] — _Rationale: [why boundaries matter]_

**Priority**: P0 | P1 | P2
**Design Ref**: §[section.number]
**Verification**: [Test approach]

---

### 3.3 [Error Handling & Edge Cases]

#### Requirement 3.3.1: [Error Scenario Name]

**User Story**: As a [role], I want [graceful degradation] so that [user impact is minimized].

**Acceptance Criteria**:

1. WHEN [upstream service] is unavailable for more than [N seconds] the system SHALL [fallback behavior] — _Rationale: [availability target]_
2. IF [invalid input is received] THEN the system MUST [reject with specific error code and message] AND SHALL NOT [unsafe behavior] — _Rationale: [security/correctness]_
3. WHEN [concurrent access creates conflict] the system SHALL [resolution strategy] — _Rationale: [data integrity]_

**Priority**: P0
**Design Ref**: §[section.number]
**Verification**: [Chaos/fault injection test approach]

---

## 4. Cross-Cutting Concerns

### 4.1 Performance Requirements

| Metric | Target | Measurement Point |
|--------|--------|-------------------|
| Latency (p50) | [X ms] | [Where measured] |
| Latency (p99) | [X ms] | [Where measured] |
| Throughput | [X TPS] | [Steady state vs peak] |
| Error Rate | < [X%] | [What counts as error] |

### 4.2 Security Requirements

- The system SHALL [authentication requirement] — _Rationale: [threat model reference]_
- The system MUST [authorization requirement] — _Rationale: [principle of least privilege]_
- The system SHALL NOT [prohibited data handling] — _Rationale: [compliance requirement]_

### 4.3 Observability Requirements

- The system SHALL emit [specific metric] on every [operation] — _Rationale: [operational visibility]_
- The system SHALL log [specific event] at [log level] with [structured fields] — _Rationale: [debugging in production]_
- WHEN [alarm condition] the system SHALL trigger [alarm] — _Rationale: [SLA enforcement]_

---

## 5. Open Questions

| # | Question | Impact if Unresolved | Proposed Resolution | Status |
|---|----------|---------------------|--------------------:|--------|
| 1 | [Question about ambiguous requirement] | [What breaks] | [Suggested answer] | Open |
| 2 | [Question about edge case] | [What breaks] | [Suggested answer] | Open |

---

## 6. Revision History

| Date | Author | Change |
|------|--------|--------|
| [Date] | [Name] | Initial draft |
| [Date] | [Name] | Resolved open questions from requirements-analyzer |
| [Date] | [Name] | Approved by [reviewer] |
