# 05 — Production-Ready Practices with Claude Code

Claude Code makes it easy to produce *a lot* of code quickly. The job of this
chapter is to make sure that code is also **correct, secure, reviewable, and
maintainable**. Speed without these is a liability.

The golden rule: **you are the engineer; Claude is the fast pair-programmer.**
You own every line that lands in `main`.

---

## 1. Always give Claude a way to verify its own work

Claude is dramatically more reliable when it can *check* the result instead of
guessing. Before asking for a change, make sure one of these exists:

- **Tests** — unit/integration tests it can run and read failures from.
- **A type checker / linter** — `tsc`, `mypy`, `ruff`, `eslint`.
- **A runnable app** — a dev server, a CLI command, a Docker container.
- **Screenshots / logs** — for UI or runtime behavior.

> Rule of thumb: if *you* can't tell whether a change works without running
> something, neither can Claude. Wire that "something" up first.

### Test-Driven Development works especially well

A reliable loop:

1. "Write tests for this behavior. Don't implement it yet — I expect them to fail."
2. Run the tests, confirm they fail for the right reason.
3. "Now implement until the tests pass. Don't change the tests."
4. Review the diff, then commit.

Telling Claude *not* to touch the tests while implementing prevents it from
"passing" by weakening assertions.

---

## 2. Keep changes small and reviewable

- One logical change per session/commit. Use `/clear` between unrelated tasks
  so stale context doesn't leak in.
- Prefer **plan mode** (read-only) for anything non-trivial: let Claude propose
  the approach, correct it, *then* let it write code. Cheap to redirect a plan;
  expensive to unwind 300 lines.
- Ask for the diff and **read it**. "I can read the diff" should be literally
  true — don't rubber-stamp.

---

## 3. Review every change — including with Claude itself

Two-layer review:

1. **Human review** of the diff. Look for: scope creep, invented abstractions,
   error handling for impossible cases, weakened tests, secrets.
2. **A second Claude pass** with fresh eyes. Use `/review` on a PR, or a
   dedicated review subagent with **read-only tools** so it can critique but not
   "fix" (and hide) its own findings. See chapter 04.

Things to actively watch for in AI-generated code:

- **Over-engineering** — abstractions, config flags, and "future-proofing" you
  didn't ask for. Push back: "remove anything the task doesn't need."
- **Phantom error handling** — `try/except` around things that can't fail.
- **Hallucinated APIs** — methods or packages that don't exist. Type checkers
  and tests catch most of these.
- **Silent assumption changes** — Claude "fixing" a test by changing what it
  asserts.

---

## 4. Security is not optional

Have Claude check its own work against the **OWASP Top 10** on anything touching
a system boundary. Concretely, flag and fix:

- **Injection** — SQL/NoSQL/command/LDAP. Use parameterized queries, never
  string-concatenated SQL. Never pass unsanitized input to a shell.
- **XSS** — escape/encode output; rely on framework auto-escaping; avoid
  `dangerouslySetInnerHTML` / `v-html` with untrusted data.
- **Secrets** — never commit `.env`, keys, tokens, connection strings. Use a
  secret manager (AWS Secrets Manager, Azure Key Vault) and reference, don't
  inline. Add a secret-scanning hook (chapter 04) or `gitleaks` in CI.
- **AuthZ/AuthN** — validate on the server, every request. Don't trust the client.
- **Dependency risk** — `npm audit`, `pip-audit`, Dependabot. Pin versions.
- **Validation at boundaries** — validate user input and external API responses;
  don't over-validate trusted internal calls.

A useful standing instruction in `CLAUDE.md`:

```
Warn me if a change introduces SQL injection, XSS, command injection, or any
OWASP Top 10 risk. Never commit secrets — reference them from a secret manager.
```

You can also run the `/security-review` skill on a branch before opening a PR.

---

## 5. Tests are part of "done"

- A feature isn't done until its tests pass — **run them before reporting done.**
- Don't mock things just to make tests green; prefer tests that exercise real
  behavior (real file I/O against a temp dir, a real test container, etc.).
- Don't assert on implementation internals — assert on observable behavior, so
  refactors don't break the suite for no reason.
- Add a regression test for every bug you fix.

---

## 6. Git discipline

- **Never work directly on `main`.** Branch first, even for small changes.
- Stage files **by name** — avoid blind `git add -A` / `git add .` so unintended
  files (and secrets) don't sneak in.
- Write real commit messages: what changed and *why*. Let Claude draft them, then
  edit.
- Never amend published commits; never force-push without explicit intent.
- Don't bypass hooks (`--no-verify`) to "get it through" — fix the underlying issue.
- Keep PRs small and focused; let Claude draft the PR description from the diff
  (the `/pr-description` skill, if available).

---

## 7. Documentation and comments

- Comment the **why**, not the **what**. One line is almost always enough.
- Keep `README` runnable: exact commands, real example I/O, a troubleshooting
  section.
- Update docs in the same change as the code — stale docs are worse than none.

---

## 8. A production-readiness checklist

Before a change is "done":

- [ ] Tests written and passing (incl. a regression test if it's a bug fix)
- [ ] Types/lints clean
- [ ] Diff reviewed by a human
- [ ] Second-pass / security review for anything at a boundary
- [ ] No secrets, no `.env`, no debug logging left in
- [ ] Error handling matches *real* failure modes (no phantom handling)
- [ ] Docs/README updated
- [ ] On a branch, small focused commits, meaningful messages
- [ ] CI green
