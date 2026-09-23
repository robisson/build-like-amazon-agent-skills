# Flow metrics

Six events, and nothing more. This document is the whole specification of what the Build Like Amazon
flow measures about itself: the closed set of events, the shape of a line, who owns each event, and the
three rules that decide whether a recorded series is worth reading at all.

The series lives in the **adopting** project, at `docs/bla-metrics.jsonl`, append-only, one JSON object
per line. **This repository does not carry one**, deliberately: a `docs/bla-metrics.jsonl` committed here
would be a series nobody measured, and a fabricated series is worse than no series. The only JSONL files
in this repository are the fixtures under `tools/tests/fixtures/metrics-*/`, which exist to test the
reader.

The reader is `python3 tools/bla-check metrics docs/bla-metrics.jsonl`.

## The six events

The set is **closed**. An `event` value outside these six is a defect in whatever wrote the line, not a
new metric, and `bla-check metrics` reports it as `FALHA [metrics-unknown-event]`.

| Event | Means |
|---|---|
| `phase_started` | a phase command began work, after its proportionality check returned Medium or above |
| `phase_completed` | that same phase saved the artefacts its `## Output` section declares |
| `spec_completed` | one spec reached execution closure and passed the marker invariant |
| `gate_approved` | a gate returned a verdict that lets the work advance |
| `gate_rework` | a gate returned a verdict that sends the work back, or an artefact returned to the same gate |
| `review_blocking_finding` | one finding was admitted at canonical severity BLOCKING |

Adding a seventh event is a change to this document, to the owner table below, to the closed set in
`tools/bla-check`, and to the fixtures — in one commit, or not at all.

## The shape of a line

Every line is one JSON **object**. Six fields are always present:

| Field | Type | Meaning |
|---|---|---|
| `event` | string | one of the six above |
| `ts` | string | ISO-8601 UTC, `YYYY-MM-DDTHH:MM:SSZ`, recorded at the moment the event happened |
| `phase` | string | the phase the event belongs to: `wb`, `design`, `spec`, `build`, `review`, `deploy`, `operate`, `learn` |
| `spec` | string or `null` | the slice name when the event belongs to one spec; `null` when it belongs to the phase as a whole |
| `level` | string | the ceremony level that admitted the event: `medium`, `large` or `new-product` |
| `source` | string | the command that emitted the line, as the user types it: `/design`, `/build`, … |

Two events carry two more fields each:

| Event | Extra fields | Meaning |
|---|---|---|
| `gate_approved`, `gate_rework` | `gate`, `verdict` | which gate, and the verdict as the surface spelled it (`APPROVED WITH NOTES`, `NEEDS REVISION`, …) |
| `review_blocking_finding` | `finding_id`, `artefact` | the finding's `F-NN` ID and the path of the report that persists it |

Example lines, in the order they would be appended:

```json
{"event": "phase_started", "ts": "2026-02-02T09:00:00Z", "phase": "design", "spec": null, "level": "medium", "source": "/design"}
{"event": "gate_rework", "ts": "2026-02-02T11:30:00Z", "phase": "design", "spec": null, "level": "medium", "source": "/design", "gate": "design-review", "verdict": "NEEDS REVISION"}
{"event": "review_blocking_finding", "ts": "2026-02-02T11:30:00Z", "phase": "design", "spec": null, "level": "medium", "source": "/design", "finding_id": "F-03", "artefact": "docs/design/checkout/review-checklist.md"}
{"event": "gate_approved", "ts": "2026-02-02T15:10:00Z", "phase": "design", "spec": null, "level": "medium", "source": "/design", "gate": "design-review", "verdict": "APPROVED"}
{"event": "phase_completed", "ts": "2026-02-02T15:20:00Z", "phase": "design", "spec": null, "level": "medium", "source": "/design"}
```

**Which fields the reader reads, and which it does not.** `event`, `ts` and `phase` are required: a line
missing any of the three is `FALHA [metrics-malformed]`, because none of the rules below can be applied
to it. `spec` keys the cycle-time pair together with `phase`; `level` and `source` are printed on the
cycle-time row, taken from the `phase_started` line of the pair. `gate`, `verdict`, `finding_id` and
`artefact` are **not aggregated by `bla-check metrics`** — no calibration exists for "how many findings
is too many", and inventing one would be exactly the fabrication rule 2 forbids. They are there so a
line can be audited against the report it came from: open the `artefact` path, find the `finding_id`.
That is their reader, and it is a human one.

## Owner table

| Event | Sole owner | Emitted when |
|---|---|---|
| `phase_started` | the phase command in flight (`/wb`, `/design`, `/spec`, `/build`, `/deploy`, `/operate`, `/learn`) | at the end of Step 0, once the proportionality check returns Medium or above |
| `phase_completed` | the same command | once its `## Output` artefacts are saved |
| `spec_completed` | `/build`, and only `/build` | at spec close, after the marker invariant passes |
| `gate_approved` | the command owning the gate: `/wb` (per stage), `/design` (Step 4, Step 5b), `/spec` (coherence review), `/build` (post-implementation review), `/review` | when the verdict is APPROVED or APPROVED WITH NOTES (any alias) |
| `gate_rework` | the same command as the gate it belongs to | when the verdict is NOT APPROVED (any alias), or when an artefact returns to the same gate |
| `review_blocking_finding` | the command that **persists** the report: `/design`, `/build`, `/review` | one line per finding admitted at canonical severity BLOCKING, carrying its `F-NN` ID |

`/review` owns no `phase_started` or `phase_completed`: it is a gate over someone else's phase, not a
phase of its own, and the phase it reviews is already emitting its own pair.

## The three rules

These are rules, not advice. A series that breaks one of them is not a weaker measurement — it is a
different thing wearing the same name.

### Rule 1 — single owner per event, declared in the emitting command

Each event has exactly one owner, and that owner is named in the emitting command's own `## Output`
section. **No command emits an event another command owns.** Where two commands could plausibly emit the
same event, the owner is the one whose `## Output` the event describes.

The failure this prevents is not a duplicate line, it is a silent one: two owners produce two lines that
look like two occurrences, and no reader downstream can tell that apart from the phase genuinely running
twice. The owner table above is the single place that assignment lives; the sentence inside each command
mirrors it.

### Rule 2 — temporal honesty

`ts` is recorded at the moment the event happens. **Never backfill in bulk.** Reconstructing a series
afterwards yields a plausible history, not a measured one, and a plausible history is indistinguishable
from a measured one to every reader who comes later — which is what makes it damaging rather than merely
useless.

- **A date with no source is absent, not plausible.** Omit the event rather than invent its time. A gap
  in the series is a fact about the series; a guessed timestamp is a lie about the work.
- **On rework, the first `phase_started` for a `(phase, spec)` pair is preserved** and no second one is
  written. The cycle time of a phase that went round a gate twice includes the rework — that is the
  measurement, not noise in it.
- Append-only plus recorded-when-it-happens implies a non-decreasing `ts`, which is why a bulk backfill
  shows up mechanically as `FALHA [metrics-out-of-order]`, and a second start as
  `FALHA [metrics-duplicate-phase-start]`.

### Rule 3 — measure outcome, not activity

Count of documents produced, of agents invoked, of lines written or of commands run is a quality measure
of nothing, and is not an event here. None of them says whether the work got better; each of them
goes up when the process gets heavier, which is the wrong direction to reward. The six events measure
what happened to the work — it started, it finished, it passed a gate, it went back — and **not
activity**.

## The Chain-1 dependency, recorded

`gate_approved`, `gate_rework` and `review_blocking_finding` became measurable **only because Chain 1
exists**. Each of the three keys on something Chain 1 produced:

- `gate_approved` and `gate_rework` key on a **legible verdict** — `AGENTS.md` → *One Severity Scale and
  One Verdict Scale* is what maps every surface's own wording onto APPROVED / APPROVED WITH NOTES /
  NOT APPROVED / INCOMPLETE, so a command can decide which of the two events a gate outcome is.
- `review_blocking_finding` keys on a **legible severity** — the same table, plus the `## Finding format`
  sections, are what make "a finding at canonical severity BLOCKING" a decidable statement rather than a
  judgement call per reviewer.

Before Chain 1 there was nothing to key on. The three events could still have been *emitted*, but not
**honestly**: each command would have been guessing what its own labels meant against every other
command's, and the resulting counts would have measured vocabulary drift rather than rework. This is why
these three events are not in a wave earlier than the one that made verdicts and severities legible.

## Graceful degradation, mandatory

Appending one line is a file write, not a runtime. It still fails sometimes: no writable tree, no `docs/`
directory, an adopter who declined to be measured.

When the write cannot happen, **state in one line that the flow measurement for this phase was not
recorded, and continue.** Measurement never blocks a phase, a gate, a build or a deployment. There is no
retry, no queue and no compensating write later — a queued line written later would break rule 2, so the
event is simply absent, and its absence is visible in the series as a missing pair.

## Proportionality

Measurement applies at **Medium and above only**. Trivial and Small emit **nothing** — not a reduced set,
nothing. A typo fix that writes a metrics line has paid ceremony for no reading, and the noise it adds to
the series costs every later reader.

This is declared as the fifth knob column, **Flow events emitted**, in the ceremony ladder:
`skills/using-amazon-skills/SKILL.md` → *The ladder*. The ladder is the single place a level's cost is
declared, and it is read monotonically there like every other column.

## What is not measured, and why

| Not measured | Why not |
|---|---|
| Escaped defects | It would require linking a production incident back to the spec that caused it. The framework cannot observe that link — nothing in the flow knows which spec a given incident traces to — and inventing the link is worse than not measuring: it would produce a defect-per-spec number that looks authoritative and is assigned by guesswork. |
| Cost | Not observable by the framework. Token spend, engineer hours and infrastructure spend all live in systems the flow never sees, and a proxy derived from what it does see (events, artefacts) would be a made-up number with a currency symbol in front of it. |
| Document and agent counts | Activity, not outcome — rule 3. Both go up when the process gets heavier and neither says whether the work got better. Counting them would reward ceremony. |
| Per-artefact quality scores | There is no calibration for them in this repository, which is the same reason `bla-check artifacts` and `bla-check review` are still registered as unimplemented. A score with no calibration is a number with no meaning. |

If one of these becomes observable — a real incident-to-spec link, a real cost feed — it becomes a
proposal to change this document, the owner table and the closed set together. It does not become a
seventh event added quietly.

## Reading the series

```sh
python3 tools/bla-check metrics docs/bla-metrics.jsonl
```

It computes two things and refuses to compute anything else:

- **Cycle time per `(phase, spec)`** — the last `phase_completed` minus the first `phase_started`. An
  incomplete pair prints `n/a` and raises `AVISO [metrics-unpaired]`. **`now` is never substituted**: a
  phase that never completed has no cycle time, and filling it in with the clock would turn an open
  phase into a finished one.
- **Rework per phase** — the count of `gate_rework`.

It validates before it aggregates, and a series with any `FALHA` is **not** aggregated — an aggregate
over a series already known to be wrong is worse than no aggregate. The rules are
`FALHA [metrics-malformed]`, `FALHA [metrics-unknown-event]`, `FALHA [metrics-out-of-order]` and
`FALHA [metrics-duplicate-phase-start]`. A file that does not exist is `AVISO [metrics-file-absent]` with
exit 0: measurement is opt-in, and its absence is never a failure.
