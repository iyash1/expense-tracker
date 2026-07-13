# 08 — Common Pitfalls & Pro Tips

## Pitfalls (and the fix)

**Letting the context fill up.** Long sessions get slower and forgetful.
→ `/clear` between unrelated tasks; `/compact` to trim; delegate research to
subagents.

**Skipping the plan on big changes.** You get 300 lines going the wrong way.
→ Use plan mode first; approve a plan before any edits.

**No way to verify.** Without tests/types/a runnable app, *you* are the checker.
→ Wire up a verification gate and tell Claude to run it.

**Rubber-stamping diffs.** AI code looks confident even when wrong.
→ Read every diff. Watch for over-engineering, phantom error handling,
hallucinated APIs, and weakened tests.

**One giant prompt for a multi-part task.** Quality drops as scope grows.
→ Break it down; one logical change per session/commit.

**Auto-approving everything.** Convenient until it deploys or deletes something.
→ Keep destructive/outward-facing actions (`push`, deploy, `rm -rf`) behind
`ask`/`deny`. Reserve `bypassPermissions` for throwaway containers.

**Trusting an unknown MCP server or skill.** They can read data and act.
→ Only add ones you trust; prefer OAuth/short-lived tokens; review skills before
committing them.

**Stale CLAUDE.md.** Wrong context is worse than none.
→ Update it when you correct Claude twice on the same thing.

---

## Pro tips

- **Correct early.** `Esc` the instant Claude drifts — don't wait for it to
  finish a wrong approach. `Esc Esc` / `/rewind` to roll back.
- **Show, don't tell.** Paste the error, the screenshot, the failing test. `@` the
  exact file. Context beats description.
- **Point at a pattern.** "Do it like `@src/UserService.ts`" outperforms abstract
  rules.
- **Use a review subagent with read-only tools** so it can't "fix" (and hide)
  what it finds.
- **Let your allowlist grow.** Approve safe, repeated commands "and don't ask
  again"; run `/fewer-permission-prompts` to bootstrap it.
- **Name your sessions** (`/rename`) and `/resume` them — long-running work
  survives across days.
- **Mind cost.** `/cost` (or `/usage`) shows spend; smaller scoped tasks +
  `/clear` keep token use down. Use a cheaper model via `/model` for routine work.
- **TDD is a cheat code.** "Write failing tests first, implement until green,
  don't touch the tests."
- **Commit small and often.** Easy to review, easy to revert, easy to bisect.

---

## Quick reference — commands

| Command | Does |
|---|---|
| `/init` | generate a starter `CLAUDE.md` |
| `/clear` | wipe conversation context (use between tasks) |
| `/compact [notes]` | summarize history, keep going |
| `/context` | show context-window usage |
| `/plan` | enter read-only planning mode |
| `/goal <cond>` | keep working until a condition holds |
| `/model` | switch model |
| `/agents` | manage subagents |
| `/mcp` | manage / authenticate MCP servers |
| `/permissions` | view/edit permission rules |
| `/hooks` | view configured hooks |
| `/memory` | view/edit memory files |
| `/review` | review a PR / changes |
| `/code-review`, `/security-review` | review skills |
| `/pr-description` | draft a PR title + body |
| `/resume`, `/rename` | resume / name sessions |
| `/cost`, `/usage` | token spend |
| `/login`, `/logout` | auth |
| `/help` | list everything |

## Quick reference — keys

| Key | Action |
|---|---|
| `Shift+Tab` | cycle permission modes (default → acceptEdits → plan) |
| `Esc` | interrupt Claude |
| `Esc Esc` | checkpoint/rewind menu |
| `@` | reference a file or directory |
| `#` | append a note to memory / CLAUDE.md |
| `↑` | command history |
| `Ctrl+D` | exit session |

---

## Official docs to bookmark

- Setup: https://code.claude.com/docs/en/setup
- Quickstart: https://code.claude.com/docs/en/quickstart
- Best practices: https://code.claude.com/docs/en/best-practices
- Permission modes: https://code.claude.com/docs/en/permission-modes
- Memory / CLAUDE.md: https://code.claude.com/docs/en/memory
- Skills: https://code.claude.com/docs/en/skills
- Subagents: https://code.claude.com/docs/en/sub-agents
- Hooks: https://code.claude.com/docs/en/hooks
- MCP: https://code.claude.com/docs/en/mcp
- GitHub Actions: https://code.claude.com/docs/en/github-actions
