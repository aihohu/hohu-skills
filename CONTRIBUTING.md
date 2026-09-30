# 贡献指南

欢迎改进 HoHu Skills 的工作流、辅助脚本和文档。本文面向本仓库贡献者；应用业务模块开发从 [HoHu 文档](https://hohu.org)开始。

## 反馈问题

在 [Issues](https://github.com/aihohu/hohu-skills/issues) 中提供 Skills、Backend/Web 和宿主版本、复现步骤、预期与实际结果及脱敏输出。不要上传凭据、环境文件或业务数据。

## 开发流程

1. 阅读受影响 Skill、[实现契约](docs/business-module.md)和仓库指令，明确改动范围。
2. 新功能或重构先写设计，说明输入输出、权限边界、兼容性和验收条件。草案放在被忽略的 `.local/docs/specs/`，需要团队讨论的内容通过 Issue/PR 共享。
3. 可执行行为修改先补失败回归，再实现；运行[验证指南](docs/validation.md)中的检查。
4. 将落地行为更新到正式手册，长期取舍写入 ADR。文档修改需要核对命令、链接和双语 README。
5. PR 描述说明问题、最终行为、实际验证及剩余限制。真实模型、浏览器和宿主验证未运行时明确说明。

辅助脚本使用 Python 3.12+ 标准库；注释和文档字符串使用英文。面向维护者的正式说明以中文为主，专业术语保留英文。面向编程助手的 Skill 与参考资料保持英文。

## 提交规范

使用一句话英文 Conventional Commit 标题，例如 `docs(readme): clarify project setup`。按文件名暂存，检查 diff，通过 `git commit -s` 添加 DCO `Signed-off-by`，不添加 `Co-Authored-By` 或额外版权消息，不使用 `--no-verify`，不 amend 已推送提交。

凭据、生成的验收项目、缓存、截图及一次性报告放在被忽略的 `.local/`，不提交。保留已有许可证，贡献遵循 [Apache License 2.0](LICENSE)。提交、推送和发布分别遵守任务授权范围。
