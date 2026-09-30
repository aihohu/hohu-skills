import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/hohu-business-module"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


inspect = load("inspect_project", SKILL / "scripts/inspect_project.py")
installer = load("install", ROOT / "scripts/install.py")


class HelpersTest(unittest.TestCase):
    def test_project_skill_installs_without_business_resources(self):
        result = installer.install(self.root, "codex", apply=True, skill="hohu-project")
        target = Path(result["destination"])
        self.assertEqual(target.name, "hohu-project")
        self.assertEqual(
            (target / "SKILL.md").read_bytes(),
            (ROOT / "skills/hohu-project/SKILL.md").read_bytes(),
        )
        self.assertFalse((target / "references").exists())
        self.assertEqual(
            installer.install(self.root, "codex", apply=True, skill="hohu-project")[
                "status"
            ],
            "unchanged",
        )

    def test_unknown_skill_is_rejected_before_writing(self):
        with self.assertRaises(ValueError):
            installer.install(self.root, "codex", apply=True, skill="../outside")
        self.assertFalse((self.root / ".agents").exists())

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(dir=os.environ["HOHU_TEST_TMP"])
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def fixture(self):
        for kind, config in inspect.CONFIG["components"].items():
            folder = self.root / config["folder"]
            for filename, markers in config["capabilities"].items():
                path = folder / filename
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("\n".join(markers), encoding="utf-8")
            if kind == "backend":
                (folder / "pyproject.toml").write_text(
                    '[project]\nversion = "0.1.5"\n', encoding="utf-8"
                )
            else:
                (folder / "package.json").write_text(
                    json.dumps({"version": "0.1.5"}), encoding="utf-8"
                )
        return self.root / "hohu-admin", self.root / "hohu-admin-web"

    def test_discovery_from_nested_component_and_read_only(self):
        backend, web = self.fixture()
        secret = backend / ".env"
        secret.write_text("PRIVATE_DO_NOT_EMIT", encoding="utf-8")
        before = sorted(str(p) for p in self.root.rglob("*"))
        result = inspect.inspect(backend / "app")
        self.assertEqual(result["components"]["web"]["path"], str(web))
        self.assertEqual(result["status"], "review_required")
        self.assertNotIn("PRIVATE_DO_NOT_EMIT", json.dumps(result))
        self.assertEqual(before, sorted(str(p) for p in self.root.rglob("*")))

    def test_missing_capability_is_incompatible_even_with_matching_version(self):
        backend, _ = self.fixture()
        (backend / "app/core/tenant_scope.py").unlink()
        result = inspect.inspect(self.root)
        self.assertEqual(result["status"], "incompatible")
        self.assertTrue(result["components"]["backend"]["missing"])

    def test_unknown_version_and_dirty_tree_require_review(self):
        backend, _ = self.fixture()
        (backend / "pyproject.toml").write_text('[project]\nversion="9.0"\n')
        result = inspect.inspect(self.root)
        self.assertEqual(result["status"], "review_required")
        self.assertEqual(result["components"]["backend"]["version"], "9.0")

    def test_reviewed_commit_and_dirty_state_are_distinct(self):
        backend, _ = self.fixture()
        config = inspect.CONFIG["components"]["backend"]
        with patch.object(
            inspect,
            "git",
            side_effect=[str(backend), config["reviewed_commits"][0], ""],
        ):
            self.assertEqual(
                inspect.component(backend, "backend", config)["status"],
                "reviewed_source",
            )
        with patch.object(
            inspect,
            "git",
            side_effect=[str(backend), config["reviewed_commits"][0], " M app/main.py"],
        ):
            self.assertEqual(
                inspect.component(backend, "backend", config)["status"],
                "review_required",
            )

    def test_parent_git_repository_is_not_component_revision(self):
        backend, _ = self.fixture()
        with patch.object(inspect, "git", return_value=str(self.root)):
            self.assertIsNone(
                inspect.component(
                    backend, "backend", inspect.CONFIG["components"]["backend"]
                )["commit"]
            )

    def test_partial_explicit_paths_are_rejected(self):
        backend, _ = self.fixture()
        with self.assertRaises(ValueError):
            inspect.inspect(self.root, backend=backend)

    def test_install_does_not_copy_bytecode(self):
        source = self.root / "source"
        source.mkdir()
        (source / "SKILL.md").write_text("skill")
        cache = source / "__pycache__"
        cache.mkdir()
        (cache / "test.pyc").write_bytes(b"cache")
        project = self.root / "project"
        project.mkdir()
        with patch.object(installer, "SOURCE", source):
            result = installer.install(project, "codex", apply=True)
        self.assertEqual(result["files"], ["SKILL.md"])
        self.assertFalse((Path(result["destination"]) / "__pycache__").exists())

    def test_explicit_renamed_components(self):
        backend, web = self.fixture()
        backend.rename(self.root / "server")
        web.rename(self.root / "client")
        result = inspect.inspect(self.root, self.root / "server", self.root / "client")
        self.assertEqual(result["status"], "review_required")

    def test_no_guessing_unrelated_root(self):
        with self.assertRaises(ValueError):
            inspect.inspect(self.root)

    def test_cli_missing_capability_exit_code(self):
        self.fixture()
        (self.root / "hohu-admin/app/core/tenant_scope.py").unlink()
        run = subprocess.run(
            [sys.executable, str(SKILL / "scripts/inspect_project.py"), str(self.root)],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(run.returncode, 2)
        self.assertEqual(json.loads(run.stdout)["status"], "incompatible")

    def test_install_preview_apply_repeat_and_tool_parity(self):
        preview = installer.install(self.root, "codex", apply=False)
        self.assertEqual(preview["status"], "preview")
        self.assertFalse((self.root / ".agents").exists())
        first = installer.install(self.root, "codex", apply=True)
        self.assertEqual(first["status"], "installed")
        self.assertEqual(
            installer.install(self.root, "codex", apply=True)["status"], "unchanged"
        )
        other = installer.install(self.root, "claude", apply=True)
        self.assertEqual(
            installer.files(Path(first["destination"])),
            installer.files(Path(other["destination"])),
        )

    def test_install_preserves_user_modifications(self):
        result = installer.install(self.root, "codex", apply=True)
        path = Path(result["destination"]) / "SKILL.md"
        path.write_text("local customization", encoding="utf-8")
        with self.assertRaises(FileExistsError):
            installer.install(self.root, "codex", apply=True)
        self.assertEqual(path.read_text(), "local customization")

    def test_install_rejects_nonexistent_project(self):
        with self.assertRaises(ValueError):
            installer.install(self.root / "missing", "claude", apply=True)

    def test_install_rejects_link_outside_project(self):
        project = self.root / "project"
        outside = self.root / "outside"
        project.mkdir()
        outside.mkdir()
        try:
            (project / ".agents").symlink_to(outside, target_is_directory=True)
        except OSError:
            self.skipTest("This account cannot create directory symlinks")
        with self.assertRaises(ValueError):
            installer.install(project, "codex", apply=True)
        self.assertEqual(list(outside.iterdir()), [])

    def test_cli_install_preview_and_invalid_project(self):
        for project, expected_code in ((self.root, 0), (self.root / "missing", 1)):
            run = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts/install.py"),
                    "--tool",
                    "claude",
                    "--project",
                    str(project),
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(run.returncode, expected_code)
            if expected_code == 0:
                self.assertEqual(json.loads(run.stdout)["status"], "preview")
        self.assertFalse((self.root / ".claude").exists())


if __name__ == "__main__":
    unittest.main()
