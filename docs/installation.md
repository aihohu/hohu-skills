# 本地源码安装与维护

在线使用优先选择 `npx skills@latest add aihohu/hohu-skills` 或 `hohu skills install`。完整用户步骤、Agent 标识、更新和排错统一维护在 [HoHu 安装指南](https://hohu.org/zh/guide/cli/skills)。本页面向本地开发和离线源码场景。

## 用上游安装器验证本地源码

在准备安装的业务项目目录执行，将示例源路径替换为实际的 hohu-skills 检出目录：

```sh
npx skills@1.7.0 add /path/to/hohu-skills --skill hohu-project hohu-business-module -a codex
```

使用 `-a claude-code cursor codex opencode trae trae-cn` 可选择多个目标。带空格的路径需加引号。上游管理安装内容与锁文件，可能采用共享目录和符号链接，不要求每个 Agent 单独复制一份。重复安装或更新可能覆盖本地定制，先备份再继续。

创建项目之前，宿主必须已经能发现 `hohu-project`。可以在宿主当前打开的父工作区安装并从该工作区提出创建请求，或明确选择上游的用户级安装；不要只把 Skill 放在尚未创建的目标目录中。项目级发现范围由宿主决定。`npx skills` 安装工作流，不安装 HoHu CLI；项目创建还需要可运行的 HoHu CLI 和终端执行能力。

## 无 npm 环境的复制备用方式

保留的 Python 复制器仅适配 Codex 和 Claude Code，用于本地开发或排错，不替代上游多 Agent 安装器。需要 Python 3.12+。在 hohu-skills 根目录执行：

```sh
python scripts/install.py --tool codex --project /path/to/business-project
python scripts/install.py --tool codex --project /path/to/business-project --apply
python scripts/install.py --tool codex --project /path/to/business-project --skill hohu-project --apply
```

第一条仅预览，第二条安装业务模块 Skill，第三条安装项目 Skill。Codex 目标为 `.agents/skills/<skill>/`，Claude Code 使用 `--tool claude`，目标为 `.claude/skills/<skill>/`。目标工作区必须已存在，可作为待创建项目的父工作区。

复制器输出 `preview`、`installed` 或 `unchanged`。已有内容不同则拒绝覆盖；更新前比较定制，将原 Skill 备份到不参与宿主发现的位置再安装。卸载只移除这个 Skill 目录，保留宿主其他设置。

该脚本不建立上游锁文件，勿在同一安装目标混用两套管理方式。它不修改全局配置、AGENTS.md 或 CLAUDE.md。手动复制时保留完整的 SKILL.md、references 和 scripts。

## 发布与验证

远程入口读取 Git 仓库，本地未推送的内容不能通过仓库名安装。先验证本地安装；发布到远程后再验证官方来源，不能用本地路径测试冒充远程成功。

确认目标目录包含有效的 `SKILL.md` 及引用资源。上游提示 `No skills found` 时，即使退出码为 0 也没有安装成功；仓库可克隆但没有 Skill 内容属于发布状态问题，不应归因于网络。

安装器版本、Skill 内容和框架版本分别管理。HoHu CLI 固定安装器 1.7.0；框架兼容范围由 [compatibility.json](../skills/hohu-business-module/references/compatibility.json) 描述。上游依赖要求或 Agent 适配变化时，重新执行安装验收。
