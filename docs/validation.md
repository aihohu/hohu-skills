# 验证指南

本文面向修改工作流和辅助脚本的贡献者。辅助脚本测试验证本仓库行为；完整业务验收验证安装后的 Skill 能否指导完成实际应用开发，两者分别记录。

## 本地辅助脚本检查

需要 Python 3.12+。在独立的 Python 开发环境中安装检查工具：

```sh
python -m pip install ruff coverage
```

版本矩阵见 [CI 配置](../.github/workflows/checks.yml)。在本仓库根目录执行，示例使用 POSIX shell：

```sh
mkdir -p .local/tests .local/reports .local/cache
export HOHU_TEST_TMP="$PWD/.local/tests"
export COVERAGE_FILE="$PWD/.local/reports/.coverage"
export PYTHONDONTWRITEBYTECODE=1
ruff check . --cache-dir "$PWD/.local/cache/ruff"
ruff format --check . --cache-dir "$PWD/.local/cache/ruff"
coverage run --source=scripts,skills/hohu-business-module/scripts -m unittest discover -s tests -v
coverage report --fail-under=70
git diff --check
```

PowerShell 中先创建目录并设置环境变量，再运行相同的 Ruff、coverage 和 Git 命令；将缓存路径换为 `"$PWD/.local/cache/ruff"`：

```powershell
New-Item -ItemType Directory -Force .local/tests,.local/reports,.local/cache | Out-Null
$env:HOHU_TEST_TMP = "$PWD/.local/tests"
$env:COVERAGE_FILE = "$PWD/.local/reports/.coverage"
$env:PYTHONDONTWRITEBYTECODE = '1'
```

预期所有测试和静态检查通过，辅助脚本总覆盖率至少 70%。测试覆盖公开源码识别、自定义目录、能力缺失、未知提交、预览、重复安装、两种宿主内容一致性及已有定制保护。测试文件见 [test_helpers.py](../tests/test_helpers.py)。

## 独立项目验收

先按[本地源码安装](installation.md)将待验证的 Skills 安装到父工作区或独立测试目录，并确认 Agent 能发现它们，再通过 HoHu CLI 创建全新项目。使用独立数据库、Redis、端口和测试账号；真实模型连接仅在授权范围内使用。

先验证 `hohu-project`：从父工作区调用实际 CLI，明确选择 Backend/Web，检查标记及实际仓库；已有目录拒绝覆盖、未知组件拒绝、旧 CLI 帮助与交互差异、失败后保留文件。初始化和服务就绪必须单独验证，使用本地仓库创建只能证明创建机制，不能替代官方网络克隆或真实部署。

在新项目中向 Agent 提出一个可验证的业务需求，例如：

> 新增租户共享的工作笔记模块，支持创建和列表、普通用户权限、AI 查询及确认后创建。业务内容只需中文。

检查设计、标准目录与导入注册、迁移、Service/API、菜单和角色、语言资源、工具注册、结果投影是否完整，并执行目标项目自己的测试门禁。分别审查“明确只需中文”和“未指定语言”的请求：前者不强制英文且不改框架国际化，后者遵循目标业务惯例；AI 默认纳入交付。扩展已有模块不应引发无关目录搬迁。

更换业务模块时按实际模型增加验证：例如设备借用需覆盖同租户不同所有者隔离、并发借用唯一性、归还状态流转和旧确认快照失效。检查静态 AI 工具清单与业务 ID 的作用域规则；独立资源授权不能通过空检查或宽泛豁免替代。

| 场景 | 预期证据 |
| --- | --- |
| 普通用户创建、分页和刷新 | 页面与 HTTP 数据一致，字符串 ID、输入校验和总数正确 |
| AI 查询与写入 | 实际工具调用、确认卡片、批准后持久化结果 |
| 取消、重放和过期 | 取消或过期不写入，重复确认不重复执行 |
| 权限撤销 | 后端拒绝越权，历史结果按当前权限遮蔽 |
| 两个租户 | 查询、写入及会话访问保持隔离 |
| 角色数据范围 | 本人、部门、部门及下级、自定义、全部按目标框架解析；多角色并集、停用、空范围回退和部门调动结果一致，全部仍不跨租户 |
| 只读角色 | 页面无写入按钮，直接 HTTP 与 AI 写入均拒绝且无数据变化 |
| 确认期间撤权 | 旧确认卡无法继续写入，历史结果按当前权限重新授权 |
| 模块语言 | 用户要求的语言下页面、菜单、工具标题及确认摘要均正确；多语言请求才要求切换验证 |

另行检查自定义目录、旧框架能力缺失、用户私有数据范围和被定制的安装目录。宿主支持须在相应宿主会话验证发现与执行；仅比较安装目录不足以证明宿主行为。

## 记录与交付

在被忽略的本地报告中记录版本、命令、结果、隔离方式和未验证项。不要将真实账号、密钥或业务数据写入产品仓库。

在报告中分别列出通过、失败和未执行的场景，并链接本次证据。模型不可用时，将真实模型场景记为未验证；模拟结果与真实提供方结果分别记录。

纯文档修改按[文档维护](DOCUMENTATION.md)检查，无需重新运行数据库或真实模型测试。
