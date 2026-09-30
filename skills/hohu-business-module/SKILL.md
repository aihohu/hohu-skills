---
name: hohu-business-module
description: Build or extend a HoHu business module following project architecture, with migrations, scoped APIs, permissions, Vue pages and application AI tools. Use for business feature development in an existing HoHu source project.
---

# HoHu business module

Deliver working source changes and evidence for the user's business scenario. Keep the scope they chose; do not force the Notes example or add operations they did not request. This skill guides an external coding assistant; the AI tools it creates run inside HoHu and remain subject to HoHu authorization and confirmation.

## Establish the target

1. Read the workspace and affected components' `AGENTS.md` (and applicable host instructions). Preserve existing edits. Determine the backend, Web, and optional docs/CLI locations; a CLI project has `.hohu/project.json`, while source checkouts may be siblings or explicitly named paths.
2. Run `python <this-skill>/scripts/inspect_project.py <project>`; resolve `<this-skill>` from this file's actual location. For renamed components pass both `--backend <path>` and `--web <path>`. Inspect the JSON status, not only the exit code. The script reads fixed public source files, not environment files. It neither imports the app nor changes it.
3. Read [compatibility.md](references/compatibility.md). `reviewed_source` means a reviewed clean source snapshot, **not** runtime acceptance. For `review_required`, compare the relevant contracts with current code. For `incompatible`, resolve the missing capability before generating code that depends on it; do not silently downgrade security or upgrade the whole app.
4. Identify required functional permissions and the business data policy (tenant-shared, strictly owner-only, or role-configured scope), API operations, fields, validation, AI read/write behavior, and observable acceptance. Follow the target's permission conventions; do not silently substitute tenant isolation or a fixed owner filter for configurable role scope. Ask only for material missing business choices while continuing independent work. Existing development authorization does not require a second approval. Production changes, credentials, and external effects retain their own scope.

## Implement one vertical slice

Create/update the feature spec according to the target project's documentation rules before implementation. Record decisions, migration/rollback, API and permission contracts, and pending Plan gaps. Use English code comments and docstrings unless the target explicitly requires otherwise.

Read [module.md](references/module.md) for implementation and registration locations. Follow the project's TDD cycle and actual source APIs. Read only the relevant sections of its architecture, security and testing guidelines; do not copy those manuals into the feature spec.

Implement the requested data model and migration, Service/API, menu permissions and role mapping, typed Web requests and page. New modules follow the target's standard directory layout; existing modules retain their established layout. Follow explicit user requirements for the business module's language; when unspecified, follow the target's business module conventions. A Chinese-only module does not require English resources or changes to HoHu's own internationalization. Keep backend permission enforcement independent of button visibility. Tests must prove tenant isolation and rollback, not just successful CRUD.

Include application AI access by default for the module's actual business operations, unless the user explicitly excludes it. Read [ai-tools.md](references/ai-tools.md). Use the existing Service and Gateway, register the tool module and assistant, wire history projection authorization, and configure the dedicated test role. Do not invent extra operations merely to populate a tool set. Write tools require a side-effect-free preview and platform confirmation; a prompt saying “ask first” is insufficient. Missing model credentials leave a runtime verification gap, not a reason to silently omit AI integration.

## Validate and deliver

Read [acceptance.md](references/acceptance.md) before running checks or touching test infrastructure. Use isolated data/services and record actual commands, versions and results. Do not copy a prior tutorial's passing report into the current result. If a real model cannot be used, complete deterministic checks and explicitly retain that acceptance gap.

Report the implemented scenario, changed files, actual tests, unsupported cases and remaining steps. Update the spec only for completed work. Do not claim browser behavior from type checking, authorization from mocked permissions, or real AI success from a model's prose. Commit/push/release only within explicit user authorization and repository rules.
