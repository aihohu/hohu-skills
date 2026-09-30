# 工作流与项目检查

本文面向维护 HoHu Skills 的贡献者，说明当前仓库边界和辅助脚本行为。安装操作见[安装说明](installation.md)，验证方法见[验证指南](validation.md)。

## 选择工作流

| 任务 | Skill | 前提与结果 |
| --- | --- | --- |
| 创建、初始化、启动或排查项目 | `hohu-project` | 需要 HoHu CLI 和终端执行能力；检查实际 CLI 支持、项目目录及服务状态 |
| 新增或扩展业务模块 | `hohu-business-module` | 需要 Backend/Web 源码；完成迁移、接口、权限、页面、应用 AI 工具和验证 |

两个 Skill 可以独立安装。一个请求同时包含项目创建和业务功能时，先完成项目准备，再进入模块开发。安装步骤见[在线指南](https://hohu.org/zh/guide/cli/skills)；测试本地修改见[源码安装](installation.md)。

项目初始化可能执行数据库迁移和种子，应先准备目标数据库与配置。项目创建、初始化和服务可用分别验证；缺少模型连接时，仍可完成项目准备，但 AI 对话需要连接就绪后再验证。

业务模块遵守目标项目目录和权限规范。AI 默认接入现有 Service、Gateway 和确认机制；国际化遵从用户明确要求，未说明时沿用目标业务模块惯例。扩展已有模块时保留既有布局，框架自带国际化保持原有行为。

## 只读项目检查器

需要 Python 3.12+ 和已检出的 Backend/Web 源码，无需启动应用或数据库。在本仓库根目录执行：

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

## 安装器边界

在线安装由上游 skills CLI 管理；HoHu CLI 包装层的契约见 [Skills 安装命令](https://github.com/aihohu/hohu-cli/blob/main/docs/SKILLS-INSTALLATION.md)。

本地复制器 `scripts/install.py` 使用 Python 3.12+ 标准库，无第三方运行时依赖。它拒绝解析到项目外的目标及源资源中的链接；已有内容相同则返回 `unchanged`，内容不同则拒绝覆盖。操作步骤、目标路径和更新方式见[本地源码安装](installation.md)。

## 授权与安全边界

编码任务授权、应用用户权限与 AI 写入确认分别检查。生成的应用工具复用 HoHu Service 和 Gateway，写入必须经历无副作用预演及平台确认；权限撤销后，历史结果仍需重新授权。

安装 Skill 不会授予应用权限或模型凭据使用权。真实模型验收需要可用且获准使用的连接；没有连接时应明确记录未验证项。安装内容一致性也不能代替各宿主的实际发现和执行验证。

业务开发分别处理功能权限、租户隔离与数据范围。共享、严格本人或角色可配置范围由业务契约确定；角色范围复用目标框架启用角色的并集解析器。查询总数、直接 ID、写入、AI 预演和历史结果使用相同授权规则，确认后撤权仍须拒绝执行。验收方法见[验证指南](validation.md)。

设计理由见[架构决策](adr/0001-portable-workflow.md)。
