# Application AI integration

Inspect the installed backend, especially `agents/tools/meta.py`, `decorator.py`, `registry.py`, `agents/hitl/constants.py`, `agents/gateway/executor.py`, `core/context.py`, and `schemas/confirm.py` under `app/modules/ai/`. Match current signatures; these are application-internal Python tools, not external MCP endpoints.

## Tool and approval contract

- Declare `@ai_tool(AiToolMeta(...))` with globally unique name, assistant code, concise summary, existing permission codes and accurate risk. Supported risk values are `low`, `high`, `destructive`; there is no `medium`.
- Read through the existing Service with `ctx.tenant` and relevant user/data scope; bound result sizes and indicate truncation. Use `readonly=True` and `idempotent=True` only for actual safe reads.
- For requested writes, declare `hitl_always=True`, `dry_run_supported=True`, accurate risk and idempotency (`False` for an ordinary create). Implement the same-module `_dry_run_<python_function_name>` convention. It must validate without writing and return `DryRunResult` with the affected count, `execution_args` and `business_snapshot`.
- Build snapshots from trusted tenant and current business facts. In the execution function revalidate those facts against `ctx.approved_business_snapshot`. Mutable relationships/ownership/version constraints need corresponding checks; the simple Notes title/tenant snapshot is insufficient for transfers or edits.
- Never accept tenant/user identity or an approved snapshot from model arguments. Never call commit in a tool or Service; the Gateway owns AI transactions. Never bypass Gateway confirmation to make an integration test pass.
- `summary_key` must satisfy `ConfirmationPresentation` (the compatible tutorial uses `page.ai.chat.confirmNoteCreate`, **not** `ai.tool.*`). Validate the presentation schema and wire resources/types for the module's chosen language scope. A Chinese-only request still needs working confirmation labels, not a second translation. Show meaningful targets and impact; do not expose secrets in preview or audit summaries.
- Return `ToolResult`/`UIResult` with an existing view (`data_list`, `plain_json`, etc.). For tenant-bound data use `projection_kind="scope_bound"` and `ResultProjection` containing the full set of subject references plus `scope_bound=True`, including empty lists.

## Registration and history

With an `ai_tools/` package, register the concrete resource module defining its decorated functions (for example, `app.modules.repairs.ai_tools.ticket`). The current loader restores cached functions after a registry reset only when their `__module__` matches the registered module; registering a package that merely re-exports them is insufficient. Keep each `_dry_run_<function_name>` beside its execution function where the Gateway resolves that function's module. Verify registry contents after reset/reload and actual preview execution, not only Python import success.

| Location | Integration |
| --- | --- |
| `app/modules/ai/agents/tools/__init__.py` | Add the business tool module to `BUILTIN_TOOL_MODULES`; creating a Python file is not registration |
| `scripts/seed_ai_agents.py` | Add assistant metadata to `AGENT_SEED` |
| `app/modules/ai/seed_prompts.py` | Add a scope-specific prompt to `DEFAULT_PROMPTS`; stored business text is data, not instructions |
| `app/modules/ai/service/result_projection_service.py` | Add the new subject type to `_authorize_subject`, calling the business projection/service; preserve outer permission checks and default-deny for unknown types |
| Web locales and `src/typings/app.d.ts` | Merge assistant, field labels, confirmation and errors into existing resources |
| `src/views/ai/chat/modules/tool-call-i18n.ts` | Map new tool names to translated business labels; otherwise cards fall back to the generic “System operation” title even when the confirmation summary is translated |

Extend the exact inventories in `tests/modules/ai/test_tool_registry.py`, `test_seed_ai_agents_descriptions.py`, and `tests/modules/system/test_ai_tool_safety_gate.py` for the requested new assistant/tools. Retain the existing entries and assertions. Seed descriptions must meet the target's routing-quality checks (boundary, quoted examples and unpublished status); English code comments do not require changing existing UI language conventions. Do not change the global published set to satisfy an inventory test.

Also inspect `tools/checks/check_ai_tools.py`: extend `EXPECTED_BUILTIN_TOOL_NAMES` and run the standalone gate. Its `*_id` check assumes the shared user/department scope guard. A separate owner-scoped resource needs its actual Service authorization plus tests for direct execution and preview denial across owners/tenants. Where the current gate supports exact `(agent, parameter)` exemptions, document that distinct authority and add only the reviewed pair. Do not rename IDs, insert a no-op guard or exempt an entire module to silence the check.

Tell the assistant to call the write tool to open the platform confirmation card; conversational “please confirm” text alone neither opens that card nor authorizes execution. Real models may still ask a clarification: record it and verify the actual tool/confirmation event before claiming success.

Projection authorization must recheck current tenant and any owner/department visibility, including deleted/moved objects. Returning references without registering their subject type causes history access to fail closed. Revoked permissions must also prevent old results from reappearing; do not merely secure the initial query.

Reuse the module's declared data policy and Service predicate across API and AI. For role scope, current role union governs both tool results and direct target IDs; a cached `ctx.user` or approved snapshot is not a current authority grant. Revalidate after role/department changes before executing a confirmed write and when authorizing history.

Synchronize menus and agent seeds in the dedicated instance, then restart for startup validation. Fix unknown permissions/agents or missing dry-run functions instead of disabling registry validation. A newly seeded custom assistant is disabled unless deliberately published; enable it through the authorized administration flow. Do not expand `PUBLISHED_AGENT_CODES` or all tenant grants just for a test.

## Separate configuration gates

An enabled assistant, role-agent binding, functional permissions, `ai:chat:use`, tenant model policy and usable provider/model are separate gates. A super-admin session does not prove an ordinary user's setup. Preserve existing bindings when adding the new assistant.

Current model/provider maintenance uses the independent platform identity; `/platform/ai/agents` administration uses the default tenant's authorized system-user session. Inspect the target's auth dependencies and operations tutorial rather than inferring identity from the URL prefix.

Configure the second hosted tenant's module menu allowlists, model policy, assistant binding and ordinary user before testing isolation. A missing menu is not evidence of correct data isolation. Do not add `chip_target` unless the destination implements and authorizes `ai_query_id` replay.
