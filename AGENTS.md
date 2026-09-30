# Repository instructions

This repository owns portable HoHu coding workflows, not framework source, human tutorials, or application data. Preserve existing files and keep the canonical workflow under `skills/`; installation adapters belong under `scripts/`.

- Read the affected skill, `docs/business-module.md`, and `docs/DOCUMENTATION.md` before changing behavior. Write feature or structural designs in ignored `.local/docs/specs/` first, then update the public current-behavior guide and necessary ADRs. Keep plans and acceptance logs out of public manuals.
- Use English comments and docstrings. Keep the canonical workflow in English, maintainer guides primarily in Chinese, and both READMEs synchronized. Follow `docs/DOCUMENTATION.md` and its public inventory. Keep the skill scoped to the user's task and reference current framework contracts instead of copying whole manuals.
- Add failing behavioral tests for executable helper changes, implement, then run the commands in `docs/validation.md`. Helpers use Python 3.12+ and the standard library. Keep helper coverage >=70%.
- Use ignored workspace `.local/` directories for test roots, caches, private configuration and acceptance reports. Set `HOHU_TEST_TMP` explicitly. Never commit credentials, generated projects or test environment files.
- Report actual validation separately from untested assumptions. A structural check or old tutorial report does not prove runtime acceptance.
- Commit only when requested: English Conventional Commit title, DCO `git commit -s`, explicit file staging, no `Co-Authored-By`, no `--no-verify`. Do not push or publish without authorization.
