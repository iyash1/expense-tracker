# 06 — Stack Playbooks (JS/Node, Python, Docker, AWS, Azure)

Same Claude Code, tuned per stack. For each, the pattern is: tell Claude the
**commands**, the **conventions**, and give it a **verification gate** (tests +
types). Put the durable parts in `CLAUDE.md` (chapter 03).

---

## JavaScript / TypeScript / Node.js

**Tell Claude in CLAUDE.md:**
- Package manager (npm/pnpm/yarn) — pick one and forbid the others.
- `"strict": true` TypeScript; **no `any`** unless unavoidable and commented.
- Named exports over default exports (better refactors).
- `async/await`, never raw `.then()` chains.
- Test runner (vitest/jest) and where tests live.

**Verification gate:** `tsc --noEmit` + `eslint` + `vitest run`. Always have
Claude run these before "done".

**High-value prompts:**
```
> add a zod schema to validate the request body in @src/api/orders.ts and
  return 400 on failure; add tests for valid + invalid payloads
> tighten types: remove every `any` in @src/services, run tsc --noEmit
> this Promise chain is hard to read — convert to async/await, keep behavior
```

**Watch for:** hallucinated npm packages (check `package.json` actually has
them), missing `await` (floating promises), and over-broad `try/catch`.

---

## Python

**Tell Claude in CLAUDE.md:**
- Version (3.10+), and the tooling: `ruff`/`black` for format, `mypy` for types,
  `pytest` for tests.
- **Type hints on all function signatures.**
- Prefer `pathlib` over `os.path`; never bare `except:` — catch specific
  exceptions.
- Virtualenv / dependency manager (uv, poetry, pip-tools).

**Verification gate:** `ruff check` + `mypy` + `pytest -q`.

**High-value prompts:**
```
> add type hints and docstrings to @src/storage.py, then run mypy
> write pytest tests for load/save using tmp_path — real file I/O, no mocks
> replace os.path usage with pathlib across @src/, keep behavior identical
```

**Watch for:** mutable default arguments, broad `except Exception`, and mocks
that hide real behavior (prefer `tmp_path`, `monkeypatch`, test containers).

---

## Docker

**Use Claude for:**
- Writing **multi-stage** Dockerfiles (build stage + slim runtime).
- Shrinking images and `.dockerignore`.
- Debugging build failures (paste the build log).

**Best-practice prompts:**
```
> write a multi-stage Dockerfile for this Node app: build with the full image,
  run on node:20-slim as a non-root user, copy only what's needed
> this image is 1.2GB — analyze the layers and slim it down
> add a .dockerignore so node_modules, .git, and .env never enter the build
```

**Production checklist Claude should honor:**
- Pin base image tags (`node:20.11-slim`, not `node:latest`).
- Run as a **non-root** user.
- No secrets in `ENV` or layers — pass at runtime / use secret mounts.
- One process per container; add a `HEALTHCHECK`.
- `.dockerignore` excludes `.env`, `.git`, `node_modules`, build artifacts.

---

## AWS

Claude is strong at IaC and SDK code, but cloud changes are **hard to reverse** —
keep it in plan/review mode for anything that deploys.

**Use Claude for:** Lambda handlers, IAM policies, CloudFormation/CDK/Terraform,
boto3/aws-sdk code, debugging from CloudWatch logs.

**Prompts:**
```
> write a least-privilege IAM policy for a Lambda that reads from this S3
  bucket and writes to this DynamoDB table — no wildcards on resources
> review this CDK stack for security: public buckets, broad IAM, open SGs
> (plan mode) explain what `terraform plan` output would change here
```

**Guardrails to set:**
- **Least privilege** IAM — no `"Action": "*"` / `"Resource": "*"`. Have Claude
  flag any wildcard.
- **No hardcoded** account IDs, ARNs, access keys, or secrets — use Secrets
  Manager / SSM Parameter Store and env vars; warn, don't silently strip.
- Prefer **IAM roles** over long-lived access keys.
- Put `deploy`, `terraform apply`, `cdk deploy` behind a `ask`/`deny`
  permission rule — **never auto-approve a deploy.**

---

## Azure

Same posture as AWS: code freely, deploy deliberately.

**Use Claude for:** Functions, Bicep/ARM/Terraform, Azure SDK code, Pulumi
(Python), debugging from App Insights.

**Prompts:**
```
> write a Bicep module for a storage account with private endpoints only
> generate a Function (Python) triggered by a Service Bus queue, with
  Managed Identity auth — no connection strings in code
> review these RBAC role assignments for least privilege
```

**Guardrails to set:**
- **Never hardcode** subscription/tenant/resource IDs or connection strings —
  use config/env vars or **Key Vault references**. Flag any found; don't remove
  on your own.
- Prefer **Managed Identities** over service principals with secrets.
- Don't store secrets in App Configuration or env vars directly — reference Key
  Vault.
- Flag any **RBAC** assignment that broadens permissions; least-privilege by
  default.
- Gate `pulumi up` / `az deployment` / `terraform apply` behind confirmation —
  ask before touching shared infrastructure.

---

## Cross-cutting

- For any cloud or infra change, work in **plan mode**, review the proposed diff,
  and require an explicit confirmation step before apply. The cost of a wrong
  auto-applied infra change dwarfs the convenience of skipping the prompt.
- Connect the relevant **MCP server** (GitHub, AWS docs, a DB) so Claude works
  from real data instead of guessing — see chapter 04.
