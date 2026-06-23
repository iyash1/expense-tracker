# 03 — Project Setup: CLAUDE.md, Settings, Permissions

Three things turn Claude Code from "generic assistant" into "knows *this*
project": **CLAUDE.md** (context), **settings.json** (configuration), and
**permissions** (what it can do without asking). Set these up once per repo and
every session gets better.

---

## CLAUDE.md — persistent project memory

`CLAUDE.md` is loaded into context at the start of every session. It's where you
encode the things you'd otherwise re-explain constantly.

Generate a starting point with `/init`, then curate it. A good `CLAUDE.md` is
**short and high-signal** — it's not documentation, it's a briefing.

What belongs in it:

```markdown
# Project: <name>

## Stack
Node 20, TypeScript (strict), React 18, Postgres. AWS (Lambda, S3). Docker.

## Commands
- Install:   pnpm install
- Dev:       pnpm dev
- Test:      pnpm test         # run before reporting any task done
- Typecheck: pnpm tsc --noEmit
- Lint:      pnpm lint

## Conventions
- Named exports only; no default exports.
- async/await, never raw .then() chains.
- Validate input at boundaries with zod; don't over-validate internal calls.
- Co-locate tests as *.test.ts next to the file.

## Architecture
- src/api      HTTP handlers (thin)
- src/services business logic (testable, no I/O)
- src/db       repositories (the only place that talks to Postgres)

## Guardrails
- Never commit secrets or .env. Reference them from AWS Secrets Manager.
- Always branch off main; never push to main directly.
```

Tips:
- Keep it under ~1–2 screens. If it's huge, Claude skims it.
- Update it when you correct Claude on the same thing twice — that's a sign the
  rule belongs here.
- Use **`#`** at the start of a message in a session to append a note to memory
  quickly (e.g. `# always use pnpm, never npm`).

### The three layers of memory

| File | Scope | Commit it? |
|---|---|---|
| `~/.claude/CLAUDE.md` | **You**, every project (personal style) | no (it's in your home dir) |
| `./CLAUDE.md` | **The team**, this repo | yes |
| `./CLAUDE.local.md` | **You**, this repo only | no (gitignore it) |

They're **concatenated**, not overridden. On a direct conflict, the more specific
(project/local) wins. Put cross-project preferences (your git habits, language
defaults) in the user file; put repo facts in the project file.

---

## settings.json — configuration

Settings live in JSON files with a clear precedence (highest wins):

```
managed policy  >  CLI flags  >  .claude/settings.local.json
                >  .claude/settings.json  >  ~/.claude/settings.json
```

| File | Purpose | Commit it? |
|---|---|---|
| `~/.claude/settings.json` | your defaults for all projects | no |
| `.claude/settings.json` | team-shared project config | **yes** |
| `.claude/settings.local.json` | your personal per-repo overrides | **no — gitignore** |

Common keys:

```json
{
  "permissions": {
    "defaultMode": "acceptEdits",
    "allow": ["Bash(pnpm test)", "Bash(pnpm lint)", "Bash(git status)"],
    "ask":   ["Bash(git push *)"],
    "deny":  ["Read(.env)", "Bash(rm -rf *)"]
  },
  "env": { "NODE_ENV": "development" },
  "hooks": { }
}
```

Add `.claude/settings.local.json` and any local data to `.gitignore`.

---

## Permissions — what runs without asking

Claude asks before doing anything potentially destructive. You tune this so you
aren't spammed with prompts for safe commands, while dangerous ones still stop.

**Rules** (in `permissions`):
- `allow` — run without asking (e.g. your test/lint/build commands, read-only git).
- `ask` — always confirm (e.g. `git push`, deploys).
- `deny` — never allowed, not even on request (e.g. reading `.env`, `rm -rf`).

Patterns use `Tool(specifier)`: `Bash(pnpm test)`, `Bash(git *)`, `Read(.env)`,
`Edit(src/**)`.

**Permission modes** (cycle with `Shift+Tab`):

| Mode | Runs without prompting | Use when |
|---|---|---|
| `default` | reads only | sensitive work, getting started |
| `plan` | reads only, no edits | exploring / designing |
| `acceptEdits` | reads + edits + common file ops | iterating on code you'll review in git |
| `auto` | most things (with safety classifier) | long unattended tasks |
| `bypassPermissions` | everything, no checks | **only** in throwaway containers/VMs ⚠️ |

Practical default: work in `default`/`plan` while exploring, switch to
`acceptEdits` once you trust the direction, and lean on git to review.

> Let your allowlist grow naturally: when Claude asks about a command you'll
> always approve (like `pnpm test`), approve it "and don't ask again" — it gets
> added to your settings. The `/fewer-permission-prompts` skill can scan your
> history and propose a starter allowlist.

---

## What to commit vs. ignore

```gitignore
# Personal / secret — do NOT commit
.claude/settings.local.json
CLAUDE.local.md
.env
.env.*
```

Commit: `CLAUDE.md`, `.claude/settings.json`, `.claude/skills/`,
`.claude/agents/`, `.claude/hooks/`, `.mcp.json` — these are team assets and the
whole point is that everyone shares them.
