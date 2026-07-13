# 02 — Core Workflows

The difference between developers who get great results from Claude Code and
those who fight it is almost always **workflow**, not prompting tricks. This is
the loop Anthropic recommends and that scales from one-liners to large features.

## The core loop: Explore → Plan → Implement → Verify → Commit

```
        ┌─────────┐   ┌──────┐   ┌───────────┐   ┌────────┐   ┌────────┐
        │ Explore │ → │ Plan │ → │ Implement │ → │ Verify │ → │ Commit │
        └─────────┘   └──────┘   └───────────┘   └────────┘   └────────┘
         (read-only)   (no code)    (edits)        (tests)      (git)
              ▲                                        │
              └────────────────  iterate  ─────────────┘
```

### 1. Explore (read-only)

Before any edits, have Claude build a mental model. Enter **plan mode** — press
`Shift+Tab` to cycle into it (or `/plan`). In plan mode Claude can read and
search but **cannot edit**, so it's safe to let it roam.

```
> (plan mode) understand how we handle auth: look at the login flow,
  session management, and how env vars are loaded. Don't write code yet.
```

For big investigations, delegate to a **subagent** so the findings come back as
a summary instead of filling your main context (chapter 04):

```
> use a subagent to investigate how token refresh works and report back
```

### 2. Plan (still no code)

Ask for an explicit plan and *review it*. It's cheap to fix a plan, expensive to
unwind code.

```
> create a detailed implementation plan: which files change, the data flow,
  edge cases, and how we'll test it
```

Redirect as needed ("don't add a new abstraction — extend the existing
`Repository` class"). Approve only when the plan is right.

### 3. Implement

Exit plan mode (`Shift+Tab`) into `default` or `acceptEdits`. Let Claude write
the code against the agreed plan. Keep the scope tight; if it starts inventing
extras, stop it.

### 4. Verify — the step people skip

**If Claude can't check its work, you are the verification loop.** Give it
something runnable and tell it to use it:

```
> implement it, then run `npm test` and fix any failures
> after the change, run the dev server and screenshot the dashboard
```

You can set a standing goal that Claude works toward until it holds:

```
> /goal tests pass and `tsc --noEmit` is clean
```

### 5. Commit

```
> commit on a new branch with a descriptive message, then open a PR
```

Read the diff first. See chapters 05 and 07 for review and CI gates.

---

## When to skip planning

If the change fits in one sentence — a typo, a rename, one log line — planning is
overhead. Reserve the full loop for: unfamiliar code, multi-file changes, or an
uncertain approach.

---

## Managing context (your real constraint)

Claude has a large but finite context window, and **performance degrades as it
fills with stale, irrelevant history.** Treat context as a budget.

- **`/clear` between unrelated tasks.** This is the highest-leverage habit. Start
  each new task with a clean slate.
- **`/compact [instructions]`** summarizes the conversation when you want to keep
  going but trim history: `/compact keep the API contract and test commands`.
- **`/context`** shows current window usage.
- **Delegate to subagents** for research-heavy detours — they run in their own
  context and return only the conclusion.
- **`@`-reference precisely.** Pull in the two files that matter, not a whole
  directory.

> Symptom of context bloat: Claude forgets a decision from earlier, repeats work,
> or gets slower/vaguer. Fix: `/clear` and restate the task crisply.

---

## Checkpoints and undo

- **`Esc`** interrupts immediately.
- **`Esc Esc`** (or `/rewind`) opens the checkpoint menu — restore the
  conversation, the code, or both to an earlier point. This makes experimentation
  cheap: try an approach, rewind if it's wrong.

---

## Prompting patterns that pay off

- **Point at an example:** "Follow the pattern in `UserService.ts` for the new
  `OrderService`." Concrete patterns beat abstract instructions.
- **Front-load context:** paste the error, link the doc, `@` the file. Don't make
  Claude guess what you can just show it.
- **State constraints up front:** "no new dependencies", "keep it in this file",
  "don't change the public API".
- **TDD framing:** "write failing tests first, then implement until they pass,
  don't modify the tests" (chapter 05).
