# 04 — Extending Claude Code: Skills, Subagents, Hooks, MCP

Out of the box Claude Code is powerful; these four mechanisms make it *yours*.
This chapter is the practical overview — the companion document
[`../Claude-Code-Advanced-Concepts.docx`](../Claude-Code-Advanced-Concepts.docx)
goes deeper with worked examples.

| Mechanism | One-line definition | Reach for it when… |
|---|---|---|
| **Skill** | Reusable instructions injected into the current context | you repeat the same workflow ("run our tests and interpret them") |
| **Subagent** | A separate Claude with its own context + tools | a task is research-heavy or you want tool isolation |
| **Hook** | A command that fires deterministically on a lifecycle event | you need a guarantee (lint, secret-scan, block a command) |
| **MCP** | A protocol to connect external tools/data | you want Claude to use GitHub, a DB, Sentry, Playwright, etc. |

---

## Skills

A skill is a folder with a `SKILL.md` that Claude loads when relevant. It
**automatically becomes a slash command** from the folder name.

```
.claude/skills/run-tests/SKILL.md   →   /run-tests
```

```markdown
---
name: run-tests
description: Run the test suite and explain failures in plain English.
---
1. Run `pnpm test`.
2. Summarize pass/fail counts.
3. For each failure, explain the cause and propose a fix.
```

**Who can invoke it** — two frontmatter keys:

| Frontmatter | User via `/cmd`? | Claude auto-invokes? | Use for |
|---|---|---|---|
| *(neither, default)* | ✅ | ✅ | normal skills |
| `disable-model-invocation: true` | ✅ | ❌ | side-effecting actions you time yourself (deploy/release) |
| `user-invocable: false` | ❌ | ✅ | background conventions you don't want to trigger by hand |

`allowed-tools:` pre-approves tools (skips prompts); `disallowed-tools:`
restricts. Great built-in skills to know: `/code-review`, `/security-review`,
`/pr-description`.

---

## Subagents

A subagent runs in an **isolated context window** and returns only its final
result — perfect for "search 30 files and tell me the answer" without polluting
your main thread. Defined in `.claude/agents/<name>.md`:

```markdown
---
name: code-reviewer
description: Reviews changes against our conventions. Use proactively after edits.
tools: Read, Grep, Glob          # read-only: it critiques, it can't "fix & hide"
---
You review code against CLAUDE.md conventions. Report file:line issues only.
```

- **Automatic delegation** is driven by `description` — add "use proactively" to
  encourage it.
- **Manual:** "Use the code-reviewer subagent on my changes", or `@`-mention it.
- **Tool restriction** (`tools` allowlist) enforces least privilege — a reviewer
  with no Edit tool can't quietly rewrite code to bury a problem.

---

## Hooks

Hooks are commands that fire **deterministically** at lifecycle events — they
*always* run, unlike instructions Claude may forget. Registered in
`settings.json` under `hooks`.

```json
{
  "hooks": {
    "PostToolUse": [
      { "matcher": "Edit",
        "hooks": [{ "type": "command", "command": "bash .claude/hooks/lint.sh" }] }
    ],
    "PreToolUse": [
      { "matcher": "Bash",
        "hooks": [{ "type": "command", "command": "bash .claude/hooks/guard.sh" }] }
    ]
  }
}
```

Key events: `PreToolUse` (can **block**), `PostToolUse` (feeds output back),
`UserPromptSubmit`, `Stop`, `SessionStart`, `SubagentStop`. Hooks receive a
**JSON payload on stdin** (`tool_name`, `tool_input`, `cwd`, …). Block an action
with **exit code 2** (stderr becomes the reason Claude sees), or emit a JSON
decision. Classic production uses: auto-format on edit, block commits containing
secrets, reject `git push` to `main`, run the type-checker after every change.

---

## MCP (Model Context Protocol)

MCP connects Claude to external systems — GitHub, databases, Sentry, AWS docs,
browsers. Add servers with the CLI:

```bash
# Local stdio server (runs as a subprocess)
claude mcp add playwright -- npx -y @playwright/mcp@latest

# Hosted HTTP server
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp

# Team-shared: commit a .mcp.json at the repo root (scope project)
claude mcp add --scope project github -- npx -y @modelcontextprotocol/server-github
```

Manage with `/mcp` in-session (list, authenticate via OAuth) and
`claude mcp list / get / remove` from the shell. Scopes: `local` (you, this repo),
`project` (committed `.mcp.json`, whole team), `user` (you, all repos).

> Security note: MCP servers can read data and take actions. Only add servers you
> trust, prefer OAuth/short-lived tokens over static secrets, and never paste a
> long-lived credential into a committed `.mcp.json`.

---

## How they compose

- A skill can run inside a forked subagent (`context: fork`).
- A subagent can preload skills and define its own hooks.
- A hook can itself invoke a prompt or subagent (`type: "agent"`).
- Everything here is committed to the repo, so it works identically in CI
  (chapter 07).
