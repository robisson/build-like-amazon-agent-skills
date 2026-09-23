# Changelog

This library is distributed by copying: an adopter copies `skills/`, or one harness command directory, into
their own project. Until now the only version anywhere was the `version` field in
`.claude-plugin/plugin.json`, which a copy-based adopter never sees, so nobody could tell what they had
copied. The marker is now `VERSION` at the repository root — one line, a bare `x.y.z` string, readable with
`cat`. `.claude-plugin/plugin.json` carries the same string, and the `version-agreement` step of
`.github/workflows/check.yml` fails the build if the two ever disagree or if the newest heading below stops
naming the current version.

## The limitation, stated as a rule

**A normal pull request does not write this changelog. Only a change that affects users does.**

A changelog that records every commit is a second, worse `git log`: it grows faster than anyone reads it, and
the one entry a reader needed is buried under typo fixes. So a pull request that corrects a sentence, renames
an internal heading, adds a predicate that changes no behaviour, or edits planning state writes **nothing**
here. An entry is owed only when the change alters what an adopter of this library does, reads or runs — a new
or removed command, a changed gate, a renamed artifact path, a new deterministic check they will now see fail,
a new CLI subcommand.

This is the one deliberate exception to *Keep the Documentation Truthful in the Same Commit* in `AGENTS.md`:
that section requires every cross-reference to move in the same commit as the thing it names, and this file is
exempt from the "every commit" half of it. When an entry **is** owed, it is still written in the same commit as
the change — the exemption is about which changes owe an entry, never about deferring one that does.

Dates come from `date +%Y-%m-%d` at the moment the entry is written. A guessed or backdated date is a lie with
a plausible shape, which is worse than no date.

<!-- Version headings are deliberately `## <x.y.z> — <date>`, WITHOUT square brackets. In CommonMark
     `## [0.2.0]` is a shortcut reference link, so it trips MD052 (undefined reference label) — and adding a
     definition block to silence MD052 then has to be maintained forever or it trips MD053 (unused
     definition). Both rules are enabled in .markdownlint-cli2.jsonc. Do not "fix" these headings back into
     brackets: the brackets buy nothing here, because no heading links anywhere. -->

## 0.2.0 — 2026-09-22

A minor bump: user-visible behaviour changed across three waves of work and nothing was removed. No command,
phase, gate, severity label or verdict label was renamed, so an adopter on 0.1.0 can copy 0.2.0 over their
tree without re-learning anything.

What changed for a user of the library:

- **A blocking finding now blocks.** `BLOCKING` (and every alias on disk) removes the option to approve and
  advance a gate; accepting one is a row in the accepted-risk table with a mitigation, an owner and a date,
  not a sentence in chat. The canonical severity scale (BLOCKING / IMPORTANT / MINOR / QUESTION) and verdict
  scale (APPROVED / APPROVED WITH NOTES / NOT APPROVED / INCOMPLETE) are declared once in `AGENTS.md` and map
  the aliases that already existed. Nothing was renamed.
- **Review output is addressable.** Every reviewer persona ends its report with a parseable verdict block, and
  every finding carries an anchor, an ID, Impact, Confidence, a minimal fix and a Status — so a finding can be
  cited, tracked and closed instead of re-read. A report with no parseable verdict counts as BLOCKING.
- **Deterministic checks, and CI that runs them.** `tools/bla-check` ships as a standard-library Python 3 CLI
  (`links`, `tasks`, `metrics`) with its own self-test, and `.github/workflows/check.yml` re-runs on every
  pull request what used to be convention in prose: README counts against disk, skill and agent frontmatter
  shape, severity and verdict label integrity, every repository path cited in prose, relative links,
  markdownlint at a pinned version, and a secret scan. Every failure prints one `FALHA [rule-name]` line.
- **`docs/artifact-catalog.md`.** One index of every artifact the workflow produces: who writes it, where it
  lands, which template shapes it and who consumes it. Three templates were orphans before it existed; the
  catalog is checked against disk in both directions.
- **Proportionality is readable, not inferred.** The ceremony ladder in `skills/using-amazon-skills/SKILL.md`
  carries a column per knob — mandatory bar raisers, deterministic verification that runs, completion
  evidence required, iteration budget, and flow events emitted — so what a level costs is in its row. No
  level was added.
- **Implementation memory is wired to the phases that can use it.** Rule selection now runs at `/design`
  (Step 0e) and `/spec` as well as `/build`, and the `Phase` field a rule carries is what selects it, so a
  rule accepted for a phase with a capture hook can actually be selected. The 12-rule cap is unchanged and
  enforced by CI.
- **Flow metrics, six events and nothing more.** `docs/flow-metrics.md` defines an opt-in, append-only JSONL
  series (`phase_started`, `phase_completed`, `spec_completed`, `gate_approved`, `gate_rework`,
  `review_blocking_finding`) emitted only at Medium ceremony and above, with a single declared owner per
  event; `bla-check metrics` validates a series and aggregates cycle time and rework. Measurement never
  blocks: a missing file is one `AVISO` line and the work continues. This repository deliberately ships no
  series of its own — a committed one would be fabricated data.
- **The harness command directories have a parity contract.** `.gemini/commands/` and `.kiro/commands/` are
  hand-synced mirrors of the canonical `.claude/commands/`, and that is now asserted by a CI predicate
  instead of being hoped for. No generator was introduced, and no command body was replaced by a pointer: a
  pointer resolves at none of the bases the copy-based install paths produce.
- **The version marker itself**, described at the top of this file, plus this changelog and the rule that
  governs it.

Explicitly not in this release, and not planned by it: an installer, a binary, a preview channel, an install
manifest, per-file hashes, or any manifest or lockfile. There is still no `package.json`, no
`pyproject.toml`, no `requirements.txt` and no lockfile anywhere in this repository, and a CI predicate keeps
it that way.

## 0.1.0 — 2026-05-18

Initial release: the 28 skills, the 10 bar-raiser personas, the 4 architectural patterns, the 14 slash
commands across the supported harnesses, and `AGENTS.md` as the operating contract. The date is the day the
`version` field first appeared in `.claude-plugin/plugin.json` (commit `4e82db5`), read from history rather
than chosen — the release was never tagged, so this is the most precise date that exists.
