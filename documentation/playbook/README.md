# The Claude Code Playbook for Developers

A practical onboarding guide for fullstack and cloud developers (JS/TypeScript,
Node.js, Python, Docker, AWS, Azure) who are **new to Claude Code** — and want to
ship **production-ready** code with it, not just code fast.

It teaches two things at once:
1. **How to drive Claude Code well** — the tool, its workflows, and how to extend it.
2. **How to keep the output production-grade** — testing, review, security, git, CI.

---

## How to use this playbook

- **Brand new?** Read **01 → 02 → 03** in order, then start using Claude Code on a
  real task. Come back for the rest as you need it.
- **Already started?** Skim **02** (workflow) and **05** (production practices) —
  that's where most quality gains live — then set up **03** in your repos.
- **Setting up a team repo?** Do **03** (CLAUDE.md, settings, permissions) and
  **07** (CI gates), and commit your **04** extensions so everyone shares them.

Each chapter is short, opinionated, and ends with concrete actions.

---

## Contents

| # | Chapter | What you'll get |
|---|---|---|
| 01 | [Getting Started](01-getting-started.md) | Install, authenticate, first session, `/init` |
| 02 | [Core Workflows](02-core-workflows.md) | The explore→plan→implement→verify loop; managing context |
| 03 | [Project Setup](03-project-setup.md) | `CLAUDE.md`, `settings.json`, permissions, what to commit |
| 04 | [Extending Claude Code](04-extending-claude-code.md) | Skills, subagents, hooks, MCP — when and how |
| 05 | [Production-Ready Practices](05-production-best-practices.md) | Verification, review, security (OWASP), tests, git |
| 06 | [Stack Playbooks](06-stack-playbooks.md) | JS/Node, Python, Docker, AWS, Azure specifics |
| 07 | [CI/CD & Automation](07-cicd-and-automation.md) | Claude in GitHub Actions; pre-commit + hook gates |
| 08 | [Pitfalls & Tips](08-pitfalls-and-tips.md) | Common mistakes + one-page command/key cheat sheet |

**Going deeper:** the companion
[`../Claude-Code-Advanced-Concepts.docx`](../Claude-Code-Advanced-Concepts.docx)
covers subagents, skills, hooks, GitHub Actions, and user-level customization
with fully worked examples.

---

## The one-paragraph version (if you read nothing else)

Run `claude` in your project and `/init` to create a `CLAUDE.md`. For anything
non-trivial, **plan before you code** (plan mode via `Shift+Tab`), then implement,
then **make Claude verify its own work by running tests/types**. Keep tasks small,
`/clear` between them, and **read every diff**. Never let it touch `main`
directly, never commit secrets, and gate deploys behind confirmation. You own the
code; Claude just writes it faster.

---

*Stack-general by design — examples span the team's stack but the practices apply
to any repo. Claude Code specifics verified against the official docs
(code.claude.com/docs); commands and shortcuts current as of June 2026.*
