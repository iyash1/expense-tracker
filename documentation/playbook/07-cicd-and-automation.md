# 07 — CI/CD & Automation

Everything you configure locally (`CLAUDE.md`, skills, agents, hooks) is in the
repo — so it works the same in automation. This chapter covers running Claude in
CI and wiring local gates that keep `main` clean.

---

## Claude Code in GitHub Actions

The official `anthropics/claude-code-action` runs Claude in a GitHub runner. You
`@claude` it from an issue or PR comment and it reads the thread, makes changes
on a branch, and opens/updates a PR — or you give it a fixed prompt for scheduled
automation (triage, dependency bumps, doc updates).

**Setup (fastest path):** from an interactive `claude` terminal, run
`/install-github-app`. It installs the GitHub App, sets permissions, and adds the
`ANTHROPIC_API_KEY` repo secret.

**Minimal workflow** — `.github/workflows/claude.yml`:

```yaml
name: Claude Code
on:
  issue_comment:
    types: [created]
  pull_request_review_comment:
    types: [created]

jobs:
  claude:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write
      issues: write
    steps:
      - uses: actions/checkout@v4
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
```

- Trigger phrase defaults to `@claude` (configurable via `trigger_phrase`).
- Pass CLI flags through `claude_args` (e.g. `--max-turns 5 --model claude-opus-4-8`).
- Provide a fixed `prompt` for non-interactive runs (scheduled jobs).
- **Enterprise auth:** `use_bedrock: "true"` (AWS OIDC → `AWS_ROLE_TO_ASSUME`) or
  `use_vertex: "true"` (GCP Workload Identity) instead of an API key.

**Security:** the key is a **repo secret**, referenced via `secrets.` — never
inline, never committed. Scope the workflow's `permissions` to the minimum.

---

## A standard CI gate (run this regardless of Claude)

Whether code is written by a human or by Claude, the same gate protects `main`:

```yaml
name: CI
on: [pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      # --- pick your stack ---
      # Node:
      - run: corepack enable && pnpm install --frozen-lockfile
      - run: pnpm tsc --noEmit
      - run: pnpm lint
      - run: pnpm test
      # Python:
      # - run: pip install -r requirements.txt && pip install ruff mypy pytest
      # - run: ruff check . && mypy . && pytest -q
```

This is the verification loop from chapter 02, enforced for everyone. Claude's
PRs are gated by exactly the same checks.

---

## Local gates: pre-commit + Claude hooks

Catch problems before they reach CI — two complementary layers.

**1. `pre-commit` (language-agnostic, runs on `git commit`):**

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks: [{ id: trailing-whitespace }, { id: end-of-file-fixer }]
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.4
    hooks: [{ id: gitleaks }]            # blocks committed secrets
```

**2. Claude Code hooks (run during a Claude session, chapter 04):** auto-format
or type-check after every edit, block `git push` to `main`, reject commands that
touch secrets. These fire while Claude works, so it self-corrects before you ever
see the change.

> Don't let Claude bypass either layer with `--no-verify`. If a hook fails, fix
> the cause — that's the hook doing its job.

---

## Automation ideas worth setting up

- **Scheduled triage**: a workflow that runs Claude nightly to label/triage new
  issues or summarize open PRs.
- **Dependency hygiene**: Dependabot/Renovate opens bump PRs; `@claude` validates
  and fixes breakages.
- **PR review assist**: run the `/code-review` or `/security-review` skill on the
  diff and post findings as comments (`--comment`).
- **Auto-generated PR descriptions** from the diff via the `/pr-description` skill.

Keep automation **gated by the same CI** as everything else — automated code is
still code, and still needs to be green and reviewed before merge.
