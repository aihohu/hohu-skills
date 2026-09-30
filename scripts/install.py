"""Copy the canonical skill to an explicit project; never overwrite local edits."""

import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1] / "skills/hohu-business-module"
TARGETS = {"codex": ".agents", "claude": ".claude"}
SKILLS = ("hohu-business-module", "hohu-project")


def files(root: Path) -> dict[str, str]:
    result = {}
    for path in sorted(root.rglob("*")):
        if path.is_symlink() or path.is_junction():
            raise ValueError(
                "Linked skill resources are not supported by this installer"
            )
        if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc":
            result[path.relative_to(root).as_posix()] = hashlib.sha256(
                path.read_bytes()
            ).hexdigest()
    return result


def install(
    project: Path,
    tool: str,
    *,
    apply: bool = False,
    skill: str = "hohu-business-module",
) -> dict:
    if skill not in SKILLS:
        raise ValueError("Unknown skill")
    source = SOURCE if skill == "hohu-business-module" else SOURCE.parent / skill
    project = project.resolve()
    if not project.is_dir():
        raise ValueError("Project must already exist")
    destination = project / TARGETS[tool] / "skills" / source.name
    if not destination.resolve().is_relative_to(project):
        raise ValueError("Installation target resolves outside the project")
    expected = files(source)
    if destination.exists():
        if not destination.is_dir() or files(destination) != expected:
            raise FileExistsError(
                "Existing skill differs; review and back it up before installing"
            )
        status = "unchanged"
    else:
        status = "preview"
        if apply:
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(
                source,
                destination,
                ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
            )
            status = "installed"
    return {
        "status": status,
        "destination": str(destination),
        "files": sorted(expected),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--tool", choices=TARGETS, required=True)
    parser.add_argument("--skill", choices=SKILLS, default="hohu-business-module")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    try:
        result = install(args.project, args.tool, apply=args.apply, skill=args.skill)
    except (OSError, ValueError) as exc:
        sys.stderr.write(f"Installation refused: {exc}\n")
        return 1
    sys.stdout.write(json.dumps(result, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
