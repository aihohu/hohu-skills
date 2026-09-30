# HoHu Skills

[English](README.md) | [简体中文](README.zh_CN.md)

面向 [HoHu](https://hohu.org) 业务应用开发的 AI 编程 Skills。

HoHu Skills 指导编程助手通过 CLI 创建和运行项目，并开发业务模块，从数据模型、权限到 Web 页面、应用 AI 工具和验证。它在你的 HoHu 源码项目中工作，遵循项目已有的开发约定。业务模块默认接入 AI；国际化遵从你的明确要求，未说明时沿用目标业务模块惯例，不修改 HoHu 自带国际化。

## 功能特性

- **完整业务模块**：数据库迁移、Service/API、菜单权限和 Vue 页面。
- **AI 工具接入**：业务查询，以及经过 HoHu 确认流程的写入操作。
- **多租户开发**：租户范围、普通用户权限和历史结果访问检查。
- **统一工作流**：Claude Code、Cursor、Codex、OpenCode 和 TRAE 共用标准 Skill 内容。
- **项目检查**：通过只读辅助脚本识别组件版本及所需能力。

## 可用 Skills

| Skill | 用途 |
| --- | --- |
| [hohu-project](skills/hohu-project/SKILL.md) | 使用 HoHu CLI 创建、初始化、启动和排查项目 |
| [hohu-business-module](skills/hohu-business-module/SKILL.md) | 新建或扩展 HoHu 业务模块，接入 AI 工具并验证完整流程 |

## 快速开始

使用 Claude Code、Cursor、Codex、OpenCode、TRAE 或其他支持 Agent Skills 的宿主。在线安装配套的安装器 1.7.0 需要带 npm/npx 的 Node.js **22.20.0+**；Skill 中的 Python 检查脚本需要 **Python 3.12+**。

在 Agent 当前打开的工作区运行；需要创建新项目时，可先安装到父工作区：

```sh
npx skills@latest add aihohu/hohu-skills
```

按安装器提示选择 Agent 和安装范围，也可以显式指定：

```sh
npx skills@latest add aihohu/hohu-skills -a codex
```

HoHu CLI 也提供安装入口：

```sh
hohu skills install
hohu skills install --agent claude-code --agent cursor
```

该命令固定使用 `skills@1.7.0` 安装器。已安装 CLI 没有此命令时使用 npx。`@latest` 指安装器版本，不是 Skill 内容版本；远程安装读取已发布到 Git 仓库的内容。

选择安装需要的 Skill。`npx skills` 只安装工作流，项目管理还需要 HoHu CLI 及宿主的终端执行能力。创建前请确保宿主能发现父工作区的 Skill，或者自行选择用户级安装。

在已安装 Skill 的工作区启动助手并提出：

```text
创建一个 HoHu 项目叫 equipment，使用后台和 Web，初始化并启动。
然后开发设备借用模块，只需要中文。
```

也可明确点名 `hohu-project` 或 `hohu-business-module`。两个 Skill 分别处理项目生命周期和业务开发，并报告实际验证结果。CLI 非交互创建会先检查当前命令是否支持 `--component`；旧版需要交互终端或兼容版本。业务工作流的框架兼容范围为已审查的 Backend/Web **0.1.5** 源码快照，见[兼容性参考](skills/hohu-business-module/references/compatibility.md)。

完整 Agent 标识、范围、更新和排错见[安装指南](https://hohu.org/zh/guide/cli/skills)，离线开发见[本地源码安装](docs/installation.md)。远程安装要求仓库已包含 Skill，本地未推送文件不会被分发。

## 文档

- [文档索引](docs/README.md)：安装、契约及维护指南，正文以中文为主。
- [HoHu 文档](https://hohu.org)：平台使用、业务开发和部署。
- [兼容性参考](skills/hohu-business-module/references/compatibility.md)：支持的源码提交和项目检查结果。

## 参与贡献

欢迎反馈问题和改进建议。提交 [Issue](https://github.com/aihohu/hohu-skills/issues) 时，请提供组件版本、复现步骤和脱敏输出。本地检查、文档及提交约定见[贡献指南](CONTRIBUTING.md)。

## HoHu 生态

| 项目 | 职责 |
| --- | --- |
| [hohu-admin](https://github.com/aihohu/hohu-admin) | 后端与平台核心 |
| [hohu-admin-web](https://github.com/aihohu/hohu-admin-web) | Web 应用 |
| [hohu-cli](https://github.com/aihohu/hohu-cli) | 项目创建、开发和部署 |
| [hohu-admin-docs](https://github.com/aihohu/hohu-admin-docs) | 产品文档和教程 |

## 许可证

[Apache License 2.0](LICENSE)。
