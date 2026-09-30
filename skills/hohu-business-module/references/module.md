# Business module integration

Read the target's `AGENTS.md` and module conventions before choosing paths. New HoHu backend modules use `api/`, `models/`, `schemas/`, `service/` and `ai_tools/` packages with `__init__.py`, splitting resource files as needed. Keep imports, route registration, ORM discovery and tool registration consistent with that package layout. Flat Notes tutorial files illustrate behavior, not the required layout for a new module. Preserve an existing module's layout when extending it; do not restructure unrelated code.

## Contract and tests first

Define the table, API paths, permission codes, page route, input validation, tenant/owner/dept visibility and requested operations. Include the corresponding denial cases in failing tests. Notes supports only tenant-wide create/list; update/delete need their own scope checks, domain rules, permissions and tests.

Use the target's feature spec location; current Backend uses local drafts and formal `docs/` contracts, Web shares the backend feature spec. Record decisions in its required format, including counterexample and regression path. Do not mark a pending acceptance as complete.

## Backend wiring

| Concern | Source to inspect | Required outcome |
| --- | --- | --- |
| ORM and IDs | `app/db/base.py`, `app/core/id_generator.py`, nearby models | Same Base, Snowflake IDs, tenant FK/index, explicit deletion and uniqueness policies; new timestamps use UTC/timezone-aware columns |
| Tenant scope | `app/core/tenant.py`, `app/core/tenant_scope.py` | Trusted `TenantContext`; list **and count**, detail, mutations and related objects enforce the same scope |
| Input/output | `app/core/base_response.py`, nearby schemas | Reject client-owned identity/tenant fields; validate trimmed input; camelCase aliases; IDs serialized as strings |
| Service | Nearby service, `app/utils/pagination.py` | Module singleton, domain exceptions, flush allowed, no commit; transactions can roll back |
| API | `app/core/auth.py`, `app/modules/auth/service.py` | `require_permissions`, `get_current_tenant_context`; API owns successful HTTP commit |
| Routing | `app/main.py` | Include the new router; verify actual OpenAPI paths and response schema |
| Metadata | `alembic/env.py` | Import the new model so autogenerate sees it |
| Isolation audit | `app/core/tenant_inventory.py` | Register each new table in the appropriate ownership inventory, including actual unique/relationship keys; a tenant column alone does not classify the resource |
| Permissions | `app/modules/system/menu_seed.py` | Register page and buttons; synchronize menus and explicitly grant the dedicated role |

Preserve `{code, msg, data}` with success code 200; pagination is `{records, total, current, size}`. Use domain exceptions with stable error codes. Reuse JWT and request handling; do not introduce separate authentication. SQL must be ORM/parameterized. Tenant identity comes from authenticated context, never request/LLM arguments.

Generate an Alembic revision only against the confirmed dedicated database. Review every operation before upgrading; unrelated drops usually mean missing model imports or an incorrect baseline. Check upgrade and downgrade/data preservation appropriate to the change. Never substitute startup `create_all()` or Marketplace/Lowcode migration runners for core schema evolution.

The reviewed backend has exact release-chain tests in `tests/test_release_migration_roundtrip.py`. Extend the explicit chain for the new revision and test its roundtrip; keep historical migration tests tied to their original revision (for example, the settings split must not accidentally test the newest business migration). Do not weaken exact assertions or skip old data-preservation checks.

Update `tests/core/test_tenant_inventory.py` with the actual new tenant-owned table and retain the disjoint ownership and tenant-leading index checks. Run the tenant isolation audit regression so an unclassified model cannot pass unnoticed.

Menu synchronization is not role authorization. Do not grant all permissions or widen published capabilities merely to make acceptance pass. For hosted tenants inspect `app/modules/system/hosted_menu_seed.py`: route/button allowlists and per-tenant synchronization are distinct from the default tenant's menu.

## Functional and data permissions

Treat functional permission, tenant boundary and business data scope as separate checks. Reuse the target's permission dependency for each operation. Specify whether records are tenant-shared, strictly owner-only, or governed by role data scope; preserve intentional existing policies. Broadening scope changes the business contract and must be explicit in the spec.

For role-configured scope, inspect `app/utils/data_scope.py` and the current authority loader in `app/modules/auth/service.py`. The reviewed resolver unions enabled roles' SELF/DEPT/DEPT_AND_SUB/CUSTOM/ALL scopes; legacy `get_best_scope` is not the runtime resolver. ALL and super-admin do not remove the tenant filter. No-role/empty-scope fallback follows the framework, not a new local algorithm.

Choose the resource's actual scope key. A model with a department field can use `get_data_scope_filters`; a reporter-owned resource can filter its reporter ID with the resolver's `accessible_user_scope`. Do not apply User-model filters directly to a different table. Document whether scope follows current user departments or a stored business department, including transfer behavior. Client/LLM input cannot set ownership or authority.

Use the same Service predicate for rows/count, direct IDs, mutations, AI preview/execution and history projections. Load current authority at sensitive execution/replay boundaries; an earlier confirmation does not preserve revoked permissions. A visible button or permitted list endpoint does not authorize every record. Keep creation identity and existing state/version constraints independent of broader read/write scope.

## Web wiring

Use `src/service/api/<module>.ts` through the existing request client; export through its API barrel where appropriate. Define `Api.<Module>` types in `src/typings/api/`. Keep IDs as strings and derive the contract from OpenAPI. Put the page in `src/views/<module>/index.vue`; reuse Naive UI, existing auth hooks, validation, pagination and error handling. Handle empty/loading/failure, repeated submission and stale list responses.

Follow explicit language requirements; otherwise follow the target's business module conventions. For a Chinese-only module, do not require English translations or alter HoHu's language selector, built-in resources or global fallback. Use supported literal labels or loaded module resources, including required types. When multilingual resources are needed, wire the requested locales under `src/locales/langs/` and `App.I18n.Schema` in `src/typings/app.d.ts`; a new locale file alone is not loaded. Check page, route, permission labels, assistant/tool labels, confirmation summaries and stable errors. User data is not a translation key.

The dev server generates Elegant Router files on page changes. Start it and wait for generation before type checking a new page. Inspect the local script before using `pnpm gen-route`: the reviewed Web version maps it to an interactive route scaffold prompt, not a non-interactive refresh command. Do not hand-edit generated routes as the business extension point. The menu's component must match the resulting route (Notes: `layout.base$view.notes`).

Validate with an ordinary role/user as well as the administrator. Refresh login after grants. Test direct HTTP denial even if the create button is hidden. UI permissions and backend permissions must refer to the same codes.
