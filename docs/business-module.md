# 工作流与辅助脚本契约

本文面向维护 HoHu Skills 的贡献者，说明当前仓库边界和辅助脚本行为。安装操作见[安装说明](installation.md)，验证方法见[验证指南](validation.md)。

## 仓库职责

`skills/hohu-project/` 负责通过 CLI 创建、初始化、启动和排查项目；`skills/hohu-business-module/` 负责业务模块开发，包含参考资料和只读项目检查脚本。两个目录均可独立安装；项目创建请求包含业务功能时衔接模块开发工作流。根目录 `scripts/` 保留本地复制备用工具，`tests/` 验证辅助脚本行为。

工作流覆盖需求和设计、模型与迁移、Service/API、权限、Web 与国际化、应用 AI 工具和验收。按用户选择的业务范围实施，Notes 只是租户共享创建/列表的参考案例。

新模块遵守目标 AGENTS 的标准目录，已有模块保持既有布局；不能将教程的平铺示例当作新模块目录模板。模块国际化遵从用户明确要求，未说明时沿用目标业务模块惯例，不修改框架国际化。AI 业务工具默认接入，复用 Service、Gateway、权限及确认机制；用户明确排除时才跳过。不新增能力配置或选择菜单。

项目工作流先检查实际 CLI 帮助。支持 `--component` 的 CLI 可非交互选择组件，旧版使用交互终端或兼容版本，不修改 CLI 内部实现。初始化可能执行迁移和种子，必须先核实数据库等环境。启动需保留前台会话并验证实际服务，不能以创建目录代替启动成功。模型不可用与项目初始化失败分别报告。

框架契约由 Backend/Web 源码及其正式规范维护；人类读者的业务教程由 `hohu-admin-docs` 维护；项目生命周期由 `hohu-cli` 管理。本仓库不提供 MCP 服务，安装过程不创建应用服务。

## 只读项目检查器

在本仓库根目录执行：

```sh
python skills/hohu-business-module/scripts/inspect_project.py /path/to/business-project
```

自定义组件目录时显式提供两个路径：

```sh
python skills/hohu-business-module/scripts/inspect_project.py /path/to/business-project --backend /path/to/backend --web /path/to/client
```

检查器读取固定的公开版本/源码文件和 Git 元数据，输出组件路径、版本、提交、工作区变更状态、缺失能力及兼容性。它不导入应用，不读取环境文件，不连接数据库或运行迁移。

| 兼容性状态 | 含义与处理 |
| --- | --- |
| `reviewed_source` | 匹配已审查且干净的源码快照，可以继续模块开发 |
| `review_required` | 提交、版本或本地改动与基线不同，需审查相关契约后继续 |
| `incompatible` | 缺失所需能力，先解决能力差异再使用相关开发流程 |

退出码 0 表示结构检查通过，1 表示输入或目录结构错误，2 表示缺失能力。退出码 0 仍可能伴随 `review_required`；调用者必须读取 JSON 状态。源码标记匹配不等于运行正确或通过安全验收。

自动发现限定于 CLI 项目标记或标准组件目录，不递归选择无关项目。支持的版本及精确提交统一维护在[兼容性清单](../skills/hohu-business-module/references/compatibility.json)，不在其他文档复制提交清单。

## 在线安装入口

标准入口为 `npx skills@latest add aihohu/hohu-skills`；HoHu CLI 的 `hohu skills install` 固定调用 `skills@1.7.0`，共用上游的 Agent 适配及管理记录。包装层契约由 hohu-cli 的 `docs/SKILLS-INSTALLATION.md` 维护，用户步骤统一在 [HoHu 文档站](https://hohu.org/zh/guide/cli/skills)。上游可能覆盖已有定制，不能套用本地复制器的拒绝覆盖承诺。

## 本地复制备用工具

`scripts/install.py` 要求显式指定已存在的项目及 `codex` 或 `claude`。`--skill` 选择两个 Skill 之一，默认 `hohu-business-module` 以兼容旧调用。默认预览，`--apply` 执行复制。两种宿主获得相同内容，目标目录见[安装说明](installation.md)。

已有内容相同则返回 `unchanged`，内容不同则拒绝覆盖。拒绝解析到项目外的目标和源资源中的链接。安装器不修改全局配置、`AGENTS.md` 或 `CLAUDE.md`。

辅助脚本使用 Python 3.12+ 标准库，无第三方运行时依赖。

## 授权与安全边界

编码任务授权、应用用户权限与 AI 写入确认分别检查。生成的应用工具复用 HoHu Service 和 Gateway，写入必须经历无副作用预演及平台确认；权限撤销后，历史结果仍需重新授权。

安装 Skill 不会授予应用权限或模型凭据使用权。真实模型验收需要可用且获准使用的连接；没有连接时应明确记录未验证项。安装内容一致性也不能代替各宿主的实际发现和执行验证。

业务开发分别处理功能权限、租户隔离与数据范围。共享、严格本人或角色可配置范围由业务契约确定；角色范围复用目标框架启用角色的并集解析器。查询总数、直接 ID、写入、AI 预演和历史结果使用相同授权规则，确认后撤权仍须拒绝执行。验收方法见[验证指南](validation.md)。

设计理由见[架构决策](adr/0001-portable-workflow.md)。
