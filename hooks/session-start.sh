#!/bin/sh
# SessionStart hook of the Claude Code plugin. A plugin's CLAUDE.md is never loaded as context, so the
# rules an installed adopter needs are printed from it here — CLAUDE.md stays their single source — and
# the plugin root is announced so the `skills/`, `agents/`, `patterns/` and `AGENTS.md` paths cited by
# the commands resolve outside this repository. Stdout of a SessionStart hook becomes session context.
root=${CLAUDE_PLUGIN_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}

printf '%s\n' "# Build Like Amazon (BLA) plugin" ""
printf '%s\n' "BLA plugin root: $root"
printf '%s\n' "Every \`skills/\`, \`agents/\`, \`patterns/\`, \`templates/\` and \`AGENTS.md\` path cited by a BLA command, skill or rule below is relative to that root, not to the working directory. Flow artifacts (\`.bla/\`) are written in the working directory. Operating behaviors: \`$root/AGENTS.md\`. Router for ambiguous requests: the \`using-amazon-skills\` skill." ""
awk '/^## Critical Rules/ { on=1 } /^## Key Files/ { on=0 } on' "$root/CLAUDE.md"
