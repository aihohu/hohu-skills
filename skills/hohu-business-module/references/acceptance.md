# Acceptance and evidence

Use project-defined local output directories. Where none exist, use an ignored `.local/` with `projects/`, `tests/`, `cache/`, `browser/`, `reports/`, and `private/`. Keep credentials, environment files and raw model responses out of tracked artifacts. Specify pytest `--basetemp`, cache and browser output paths explicitly. Do not move installed or running projects.

For new-project acceptance, use the actual `hohu --help`/`hohu create --help` interface (CLI 0.1.13 exposes `hohu create`, `hohu init`, `hohu dev`). Create Backend/Web in the designated local projects directory. Give PostgreSQL, Redis, application and frontend independent ports and storage. Confirm the URLs target that instance before migrations, seeds or tests. Do not copy an existing application's `.env` or data. Reusing model credentials requires authorization for this new use; it is not implied by an earlier test.

Verify the installed `SKILL.md` and referenced files, not just an installer exit code: the upstream installer can report no skills with exit 0. Distinguish a clone/network failure from a reachable repository that does not yet contain the unpublished local Skill. Inspect the Web dev script's actual Vite mode before writing an environment override; mode-specific files can override `.env.local` and accidentally route verification to a different backend.

## Validation layers

1. **Source/helper checks:** inspect project compatibility; verify new module directories against the target's AGENTS, including imports, ORM discovery and AI registration after package splitting. Existing modules follow their current layout. Review the diff and run lint/format/typecheck. Run tool metadata validation (`python -m tools.checks.check_ai_tools` in the compatible backend). A successful static check is not runtime proof.
2. **Regression suite:** run failing tests before implementation, then targeted and full relevant suites and repository coverage gates (currently >=70%). Use transactional fixtures; test scope on list and count, direct IDs and relationships, input spoofing, ID serialization and rollback. SQLite examples are supplemental and cannot prove PostgreSQL migration or Gateway behavior.
3. **Migration/API/Web:** upgrade the dedicated PostgreSQL instance, check only intended schema changes, exercise OpenAPI and ordinary-user HTTP permissions, then use the page to create and reload data. Check menu/page/assistant/card labels in the module's requested languages; switch locales only when multilingual behavior is in scope. Do not change framework internationalization for a single-language module. Check refresh, invalid input, forbidden actions and duplicate submission.
4. **AI integration:** run the scenarios below through the real Gateway. Deterministic test doubles can isolate failure states but must be labeled; real-provider results require actual tool records and persisted state.

| Scenario | Evidence required |
| --- | --- |
| Read an existing page-created item | Actual tool name, matching string ID and bounded result |
| Propose a write | Confirmation card and zero writes before approval |
| Cancel | Rejected/cancelled status, unchanged records |
| Approve a new proposal | Success, exactly one persisted change visible after login/reload |
| Replay the same confirmation | Same terminal result, no second write; not a new conversation request |
| Expire a confirmation | Actual configured TTL and expired response, zero writes |
| Revoke write permission | Direct API and AI write refused; remaining reads follow remaining grants |
| Revoke read/assistant access | Reopened history redacts or refuses formerly visible results |
| Second configured tenant | HTTP list/count, AI result and history cannot access first-tenant records |
| Mutable target changes before approval | Snapshot/version/relationship check refuses stale authorization |

Test manual assistant selection and automatic routing where both are part of the user flow. Use isolated role sessions so a second role does not mask revocation. For multi-worker confirmation, verify the supported persistent mode; do not run multiple workers with in-memory confirmation and call the result durable.

For role-configured data scope, build a small organization with self, same department, child department, custom department, unrelated users and a second tenant. Compare list/count, direct-ID writes, AI previews and persisted projections across all supported scopes. Include incomparable multi-role union, disabled roles, no-role/empty-scope fallback, department transfer and revocation between preview and approval. ALL must still exclude the second tenant. For shared or owner-only modules, test that declared policy instead; do not expand business visibility just to exercise the matrix.

Separately test a read-only ordinary role: hidden write controls, direct HTTP denial, AI write denial, and unchanged database state. Revoke read or assistant access and reopen previously successful history. Use actual role/menu/dept facts where possible; tests with mocked permissions do not prove the authorization integration. Record which cases are database regression, live HTTP/browser, deterministic Gateway, or real-provider validation.

A routing clarification that offers the correct assistant is not an executed query. Distinguish provider failures from authorization failures; record sanitized status/error codes and stop repeated model retries when the provider reports a billing or quota block. Do not expose raw provider responses or credentials, and do not purchase credit as part of acceptance.

## Completion record

Record CLI and Skill versions, Backend/Web/tutorial SHAs, clean/dirty baseline, migration revisions, executed commands, test counts/coverage and real model name (no credentials). Separate pass/fail/not run and explain blockers. Link redacted local evidence. Update only completed Plan states in the spec; include concrete source limitations. Never reuse a previous Notes acceptance as this run's result.

Stop only the dedicated processes/services created for this acceptance when appropriate; do not remove shared services or data. Leave explicit startup/cleanup instructions if preserving the instance for review. Do not publish or push as a side effect of validation.
