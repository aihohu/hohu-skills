---
name: hohu-project
description: Create, initialize, start, or troubleshoot a HoHu source project using HoHu CLI. Use when the user asks to create a HoHu project or run an existing one; business module implementation belongs to hohu-business-module.
---

# HoHu project

Turn the user's project request into a working HoHu workspace using the actual CLI. Preserve their chosen components, location and existing files. Do not introduce a feature questionnaire or change framework internationalization or tenancy settings as part of ordinary creation.

## Locate the project and CLI

Read applicable `AGENTS.md` files. For an existing project, locate `.hohu/project.json` and verify its component directories; a marker can survive a failed clone. For creation, use the requested parent directory and a new child name. Put acceptance projects and logs in the workspace's designated local directories.

Run `hohu --version`, `hohu --help` and the relevant subcommand's `--help`. Prefer the user's selected local CLI checkout when testing unpublished changes, while keeping the intended project working directory. Do not silently invoke a global version instead. If CLI is absent, inspect its official installation instructions and use an isolated tool environment supported by the machine. Do not invent an npm HoHu package or equate `npx skills` with HoHu CLI.

Confirm Git, Python/uv and Node/pnpm availability for selected components. Read their declared versions and initialization instructions rather than assuming CLI startup proves dependency compatibility.

## Create and initialize

Use the user's component selection. When unspecified, state Backend and Web as the starting assumption; add App only when requested. With a CLI exposing these options, run from the chosen parent directory:

```sh
hohu create my-project --component backend --component web --non-interactive
```

`--component` is repeatable; backend, frontend/web and app are supported. Explicit components skip selection prompts. Older CLIs may offer only interactive creation: use an available interactive terminal or a compatible CLI installation; report the limitation if neither is available. Do not monkeypatch CLI internals or guess unsupported flags. The legacy `--repo` overrides every selected component's source, so use it only for an intentional common source or a single-component test.

Check exit status, project marker and actual component checkouts. Existing paths must not be overwritten. A failed clone may leave partial files: inspect them and recover only the missing step; do not delete or silently reuse unrelated work. Retry a transient network failure once; use a local source only when authorized and record its actual revision. Keep TLS verification enabled.

Before initialization, inspect backend `.env.example`, `scripts/init.py` and component instructions. Prepare database, Redis and environment first: `hohu init` can run migrations and seeds, not just install packages. Use dedicated local services for acceptance projects. Preserve existing secrets and settings, generate required secrets locally, and never copy another application's environment or data wholesale. Report missing external credentials or infrastructure precisely while completing independent setup work.

From the project root:

```sh
hohu init
```

Verify both dependency installation and component initialization. On failure, retain logs and resume the failed step using its supported command; label any direct-command fallback. Do not report complete initialization from the project marker or final CLI message alone.

## Start and verify

For a request to run the app, use `hohu dev` from the project root. It is a foreground process: retain a managed terminal/session, capture logs, and identify only processes created for this task. Inspect `hohu dev --help` for component filtering. Check port availability; use supported component configuration or documented direct commands for custom ports, not invented CLI flags.

Inspect Web's actual dev script and Vite mode before configuring its backend URL. Confirm the effective API target, backend OpenAPI/health response and frontend page. Test login when credentials and browser access are available. Distinguish process startup, HTTP availability and verified login. Do not print whole environment files or tokens; provide the credential location or the requested test login through the authorized channel.

Keep existing AI infrastructure. Verify provider availability before claiming a working AI conversation; do not reuse another project's credentials without authorization. Missing model access does not prevent creating or starting the app.

If the request also includes business development, continue with `hohu-business-module` when installed, reading it at its discovered location. Otherwise report the missing workflow and follow the target's development rules without claiming to have invoked it. Do not add business features for a creation-only request.

Deliver the project path, components, actual CLI/source versions, executed checks, URLs, login verification status, stop/restart instructions and remaining setup. Do not deploy, publish or commit as an implicit part of local creation.
