# 01 — Getting Started

## What Claude Code is

Claude Code is an AI coding agent that runs **in your terminal** (also available
as a desktop app and IDE extensions). It can read your codebase, run commands,
edit files, run tests, use git, and call external tools — all under permission
controls you set. Think of it as a fast pair-programmer that lives where your
code lives.

It is **agentic**: you describe an outcome, and it explores, plans, edits, and
verifies in a loop — not a single autocomplete.

---

## Install

Pick one. Native installer is recommended; npm is fine if you live in Node.

```bash
# macOS / Linux / WSL
curl -fsSL https://claude.ai/install.sh | bash

# Windows PowerShell
irm https://claude.ai/install.ps1 | iex

# Homebrew (macOS)
brew install --cask claude-code

# Windows (WinGet)
winget install Anthropic.ClaudeCode

# npm (needs Node.js 18+)
npm install -g @anthropic-ai/claude-code
```

Native installs auto-update; Homebrew/WinGet need manual `upgrade`.

Verify:

```bash
claude --version
```

---

## Authenticate

Run `claude` in any project directory. On first use a browser window opens.
Choose your path:

- **Claude Pro/Max subscription** — simplest for individuals; log in with your
  Claude account. Re-auth anytime with `/login`.
- **Anthropic Console (API credits)** — pay-as-you-go, per-seat cost tracking;
  good for teams. Create a key at console.anthropic.com.
- **Cloud providers** — Amazon Bedrock (`CLAUDE_CODE_USE_BEDROCK=1`), Google
  Vertex (`CLAUDE_CODE_USE_VERTEX=1`), Microsoft Foundry
  (`CLAUDE_CODE_USE_FOUNDRY=1`). Uses your cloud credentials, no browser login.
  Relevant if your org standardizes on AWS/Azure.

Credentials are stored in your OS keychain (macOS) or `~/.claude/.credentials.json`
(Linux/Windows, locked-down permissions).

---

## Your first session

```bash
cd your-project
claude
```

Then just talk to it. Good first prompts to build intuition:

```
> give me a high-level overview of this codebase and how it's structured
> where is user authentication handled?
> run the test suite and tell me what's failing
```

Notice it asks **permission** before running commands or editing files the first
time — that's the safety model (chapter 03). Approve, and optionally tell it to
remember the approval.

### The single most important first step: `/init`

```
> /init
```

This scans the project and generates a `CLAUDE.md` — persistent project context
Claude loads every session. Edit it to capture how *your* project really works.
See chapter 03.

---

## Talking to it effectively (the 30-second version)

- **Reference files with `@`** — `explain @src/server.ts` reads the file first.
- **Paste screenshots** directly for UI bugs or design targets.
- **Pipe input** — `cat error.log | claude -p "what caused this?"`.
- **Be specific.** "Fix the login bug where users see a blank screen after
  entering wrong credentials; write a failing test first" beats "fix login."
- **Interrupt with `Esc`** the moment it heads the wrong way — don't wait.

---

## Where to go next

- **02 — Core workflows**: the explore → plan → implement → verify loop, and
  managing context.
- **03 — Project setup**: `CLAUDE.md`, settings, and permissions.
- **04 — Extending Claude Code**: skills, subagents, hooks, MCP.
- **05 — Production practices**: tests, review, security, git.
- **06 — Stack playbooks**: JS/Node, Python, Docker, AWS, Azure.
- **07 — CI/CD & automation**: Claude in GitHub Actions and pre-commit gates.
- **08 — Pitfalls & tips**: common mistakes, plus a one-page command/key cheat sheet.
