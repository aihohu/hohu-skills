# 本地源码安装与维护

本页用于测试本地修改，或在无 npm 的环境中安装已取得的 Skills 源码。通过官方仓库在线安装，见 [HoHu 安装指南](https://hohu.org/zh/guide/cli/skills)。

## 用上游安装器验证本地源码

准备好本地 hohu-skills 源码、Node.js 22.20.0+ 和 npm/npx。首次使用安装器需要访问 npm；完全离线时使用下方 Python 复制方式。

进入准备使用 Agent 的工作区，将示例源路径替换为实际的 hohu-skills 检出目录：

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

该脚本不建立上游锁文件，勿在同一安装目标混用两套管理方式。它不修改全局配置、AGENTS.md 或 CLAUDE.md。手动复制时保留所选 Skill 目录的全部内容，包括 `SKILL.md` 及其引用资源。

## 确认安装结果

在目标工作区重新打开 Agent 会话，确认能发现所选 Skill，并明确指定 `hohu-project` 或 `hohu-business-module` 发起任务。前者应先检查实际 CLI，后者应先识别目标项目及兼容性。详细场景见[验证指南](validation.md)。

本地安装用于测试工作区中的源码；通过仓库名安装读取远端内容。发布后还需按在线指南重新验证官方来源。

确认目标目录包含有效的 `SKILL.md` 及引用资源。上游提示 `No skills found` 时，即使退出码为 0 也没有安装成功；仓库可克隆但没有 Skill 内容属于发布状态问题，不应归因于网络。

安装器版本、Skill 内容和框架版本分别管理。HoHu CLI 固定安装器 1.7.0；框架兼容范围由 [compatibility.json](../skills/hohu-business-module/references/compatibility.json) 描述。上游依赖要求或 Agent 适配变化时，重新执行安装验收。
