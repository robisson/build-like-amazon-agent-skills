# Build Like Amazon — where the library's paths live in this project

The BLA skills, the phase procedures under `.kiro/skills/bla/references/` and `AGENTS.md` cite paths the
way they sit in the Build Like Amazon repository. In this project they were installed under `.kiro/`.
Whatever started the work — `/bla <phase>`, a skill typed as `/<name>`, or a skill Kiro activated on its
own — resolve every cited path through this map before you open it:

| Cited as | Open |
|---|---|
| `skills/<name>/…` | `.kiro/skills/<name>/…` |
| `.claude/commands/<phase>.md` | `.kiro/skills/bla/references/<phase>.md` |
| `agents/<persona>.md` | `.kiro/skills/bla/references/agents/<persona>.md` |
| `patterns/…` | `.kiro/skills/bla/references/patterns/…` |
| `tools/bla-check`, `AGENTS.md`, `.bla/…` | the same path, from the project root |

A phase command written `/wb`, `/design`, `/build` and so on is `/bla wb`, `/bla design`, `/bla build`
here. `docs/…` and the library's `README.md` are its own documentation and are not installed — a
`README.md` at this project's root is the project's, not the BLA skill catalogue; the installed skills
are the folders under `.kiro/skills/`. If a mapped file is missing, say so and continue from what is on
disk — never reconstruct a file you cannot read.
