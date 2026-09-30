# HoHu Skills

[English](README.md) | [简体中文](README.zh_CN.md)

AI coding skills for building business applications with [HoHu](https://hohu.org).

HoHu Skills guides coding assistants through CLI project creation and startup, then business development: data models, permissions, Web pages, application AI tools and validation. It follows your HoHu project's conventions. Business modules include AI by default; their language scope follows your explicit request, otherwise the target's business module conventions, without changing HoHu's built-in internationalization.

## Features

- **Complete business modules** — database migrations, Service/API layers, menus, permissions and Vue pages.
- **AI tool integration** — business queries and write operations through HoHu's confirmation flow.
- **Tenant-aware development** — tenant scope, ordinary-user permissions and history access checks.
- **Shared workflow** — the same standard skill content across Claude Code, Cursor, Codex, OpenCode and TRAE.
- **Project inspection** — a read-only helper identifies component versions and required capabilities.

## Available skills

| Skill | Use it to |
| --- | --- |
| [hohu-project](skills/hohu-project/SKILL.md) | Create, initialize, start and troubleshoot projects through HoHu CLI |
| [hohu-business-module](skills/hohu-business-module/SKILL.md) | Create or extend a HoHu business module, connect AI tools and validate the complete flow |

## Quick start

Use Claude Code, Cursor, Codex, OpenCode, TRAE or another supported Agent Skills host. Online installation requires Node.js **22.20.0+** with npm/npx for the paired installer 1.7.0. The skill's Python helper requires **Python 3.12+**.

Run in the workspace currently open in your agent; for a new project, install in its parent workspace first:

```sh
npx skills@latest add aihohu/hohu-skills
```

Select your agents and installation scope in the installer, or specify a target:

```sh
npx skills@latest add aihohu/hohu-skills -a codex
```

HoHu CLI also provides an installation entry point:

```sh
hohu skills install
hohu skills install --agent claude-code --agent cursor
```

This command uses the pinned `skills@1.7.0` installer. If your installed HoHu CLI does not contain the command, use npx. `@latest` refers to the installer, not the skill content; remote installation reads the published Git repository.

Select the skills you need. `npx skills` installs workflows; project management also requires HoHu CLI and the host's terminal capability. Before creation, ensure the host discovers the parent workspace's skills, or explicitly choose a user-level installation.

Start your assistant in the workspace with the installed skills and ask:

```text
Create a HoHu project named equipment with Backend and Web, initialize it and start it.
Then develop an equipment borrowing module with Chinese-only business content.
```

You can explicitly name `hohu-project` or `hohu-business-module`. They handle project lifecycle and business development respectively, reporting actual validation. Non-interactive creation first checks CLI support for `--component`; older versions need an interactive terminal or a compatible version. Business workflow compatibility targets reviewed Backend/Web **0.1.5** snapshots, listed in the [compatibility reference](skills/hohu-business-module/references/compatibility.md).

See the [installation guide](https://hohu.org/guide/cli/skills) for all agent IDs, scope, updates and troubleshooting, or [local source installation](docs/installation.md) for offline development. Remote installation requires this skill to be present in the remote repository; local unpushed files are not distributed.

## Documentation

- [Documentation index](docs/README.md) — installation, contracts and maintenance guides; these guides are maintained primarily in Chinese.
- [HoHu documentation](https://hohu.org) — platform usage, business development and deployment.
- [Compatibility reference](skills/hohu-business-module/references/compatibility.md) — supported source revisions and inspection results.

## Contributing

Bug reports and improvements are welcome. Open an [issue](https://github.com/aihohu/hohu-skills/issues) with your component versions, reproduction steps and sanitized output. Read the [contribution guide](CONTRIBUTING.md) for local checks, documentation and commit conventions.

## HoHu ecosystem

| Project | Responsibility |
| --- | --- |
| [hohu-admin](https://github.com/aihohu/hohu-admin) | Backend and platform core |
| [hohu-admin-web](https://github.com/aihohu/hohu-admin-web) | Web application |
| [hohu-cli](https://github.com/aihohu/hohu-cli) | Project creation, development and deployment |
| [hohu-admin-docs](https://github.com/aihohu/hohu-admin-docs) | Product documentation and tutorials |

## License

[Apache License 2.0](LICENSE).
