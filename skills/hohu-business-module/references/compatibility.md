# Supported source contract

Version 0.1.0 targets HoHu Backend and Web **0.1.5 at the source snapshots in [compatibility.json](compatibility.json)** and CLI 0.1.13 for project creation. Other commits, dirty trees and unknown versions require source review; older releases without tenant-scoped queries, approved business snapshots or history projection are not supported by this workflow unchanged. Marker checks only identify likely structural compatibility, not semantic correctness or security.

Python helpers require Python 3.12+ and use only the standard library. Backend/Web runtime dependencies come from their own lockfiles. A full slice needs both components. Explicit paths support renamed checkouts; automatic discovery searches ancestors for the CLI marker or standard sibling folders and never recursively picks an unrelated project.

Authority order: user scope and target instructions → current code/OpenAPI and migrations → target repository formal guidelines → this skill and compatible tutorial examples. If contracts differ, inspect and document the difference instead of patching the framework to match this skill.

Read the target backend's `docs/DEV-GUIDELINES.md`, `docs/ARCHITECTURE-GUIDELINES.md`, `docs/SECURITY.md`, `docs/TESTING-GUIDELINES.md`, and `docs/DOCUMENTATION.md` as relevant. Missing local docs can be obtained from the same revision of the public repository; do not treat an unversioned online tutorial as proof of compatibility.

Reference sources:

- [Backend reviewed snapshot](https://github.com/aihohu/hohu-admin/tree/20d065dc610428962fcf2cdaf65d7d916c4408b2)
- [Web reviewed snapshot](https://github.com/aihohu/hohu-admin-web/tree/3a8e542262a85b17aea9529404e03f5e895b2953)
- [Module tutorial](https://github.com/aihohu/hohu-admin-docs/blob/2992004/docs/guide/development/module.md), [AI integration tutorial](https://github.com/aihohu/hohu-admin-docs/blob/2992004/docs/guide/development/ai-tools.md)
- [Notes examples](https://github.com/aihohu/hohu-admin-docs/tree/2992004/examples/notes), used as a small tenant-wide create/list reference, not a general owner/department permission implementation.

The tutorial is maintained in `hohu-admin-docs`, framework contracts in Backend/Web, lifecycle in `hohu-cli`, and this task workflow in `hohu-skills`. No MCP service or CLI integration is required to install this version.
