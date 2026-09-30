"""Inspect fixed public source paths without importing or connecting to HoHu."""

import argparse
import json
import subprocess
import sys
import tomllib
from pathlib import Path

CONFIG = json.loads(
    (Path(__file__).resolve().parents[1] / "references/compatibility.json").read_text(
        encoding="utf-8"
    )
)


def git(path: Path, *args: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(path), *args],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    return result.stdout.strip() if result.returncode == 0 else None


def discover(start: Path) -> Path:
    start = start.resolve(strict=True)
    if not start.is_dir():
        raise ValueError("The project path must be a directory")
    for candidate in (start, *start.parents):
        folders = [entry["folder"] for entry in CONFIG["components"].values()]
        within_component = candidate == start or any(
            start.is_relative_to(candidate / folder) for folder in folders
        )
        if within_component and (
            (candidate / ".hohu/project.json").is_file()
            or all((candidate / folder).is_dir() for folder in folders)
        ):
            return candidate
    raise ValueError("No HoHu project found; pass --backend and --web explicitly")


def component(path: Path, kind: str, config: dict) -> dict:
    missing = []
    for filename, markers in config["capabilities"].items():
        file = path / filename
        if not file.is_file():
            missing.append(filename)
            continue
        source = file.read_text(encoding="utf-8-sig")
        missing.extend(
            f"{filename}: {marker}" for marker in markers if marker not in source
        )
    version_file = path / ("pyproject.toml" if kind == "backend" else "package.json")
    version = None
    if version_file.is_file():
        source = version_file.read_text(encoding="utf-8-sig")
        data = tomllib.loads(source) if kind == "backend" else json.loads(source)
        version = (
            data.get("project", {}).get("version")
            if kind == "backend"
            else data.get("version")
        )
    # Do not mistake a parent repository's HEAD for this component's revision.
    git_root = git(path, "rev-parse", "--show-toplevel")
    own_repo = git_root is not None and Path(git_root).resolve() == path.resolve()
    sha = git(path, "rev-parse", "HEAD") if own_repo else None
    status = (
        git(path, "status", "--porcelain", "--untracked-files=normal")
        if own_repo
        else None
    )
    dirty = bool(status) if status is not None else None
    reviewed = (
        sha in config["reviewed_commits"]
        and dirty is False
        and version == config["version"]
    )
    return {
        "path": str(path),
        "version": version,
        "commit": sha,
        "dirty": dirty,
        "missing": missing,
        "status": "incompatible"
        if missing
        else "reviewed_source"
        if reviewed
        else "review_required",
    }


def inspect(start: Path, backend: Path | None = None, web: Path | None = None) -> dict:
    if (backend is None) != (web is None):
        raise ValueError("Provide both --backend and --web for custom layouts")
    root = start.resolve(strict=True) if backend is not None else discover(start)
    paths = {"backend": backend, "web": web}
    components = {}
    for kind, config in CONFIG["components"].items():
        path = (paths[kind] or root / config["folder"]).resolve()
        components[kind] = component(path, kind, config)
    statuses = {item["status"] for item in components.values()}
    status = (
        "incompatible"
        if "incompatible" in statuses
        else "review_required"
        if "review_required" in statuses
        else "reviewed_source"
    )
    return {
        "skill_version": CONFIG["skill_version"],
        "root": str(root),
        "status": status,
        "components": components,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    parser.add_argument("--backend", type=Path)
    parser.add_argument("--web", type=Path)
    args = parser.parse_args()
    try:
        result = inspect(args.project, args.backend, args.web)
    except (OSError, ValueError) as exc:
        sys.stderr.write(f"Inspection failed: {exc}\n")
        return 1
    sys.stdout.write(json.dumps(result, indent=2, ensure_ascii=True) + "\n")
    return 2 if result["status"] == "incompatible" else 0


if __name__ == "__main__":
    raise SystemExit(main())
