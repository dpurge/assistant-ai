"""Tests for the build/install/uninstall scripts, focused on the pi target
bundling extensions/themes and only ever touching content the plugin owns."""

from __future__ import annotations

import sys
import zipfile
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import _common  # noqa: E402
import build as build_mod  # noqa: E402
import install as install_mod  # noqa: E402
import uninstall as uninstall_mod  # noqa: E402


@pytest.fixture
def dist(tmp_path, monkeypatch):
    """Redirect dist/ to a tmp dir so tests never touch the real one."""
    d = tmp_path / "dist"
    monkeypatch.setattr(_common, "DIST_DIR", d)
    monkeypatch.setattr(build_mod, "DIST_DIR", d)
    return d


def _names(zip_path: Path) -> set[str]:
    with zipfile.ZipFile(zip_path) as z:
        return set(z.namelist())


def test_pi_zip_bundles_skills_extensions_and_themes(dist):
    zip_path = build_mod.build_one("pi", _common.load_version())
    names = _names(zip_path)

    assert "extensions/research.ts" in names
    # The workflow harness ships as a folder: a generic engine, a registry of
    # named workflows, and the per-workflow modules. The old workflow.md doc was
    # removed when it became a real extension.
    assert "extensions/workflow/index.ts" in names
    assert "extensions/workflow/engine.ts" in names
    assert "extensions/workflow/registry.ts" in names
    assert "extensions/workflow/pi-executor.ts" in names
    assert "extensions/workflow/workflows/phraseforge-mdx.ts" in names
    assert "extensions/workflow.md" not in names
    assert "themes/dpurge-dark-default.json" in names
    assert any(n.startswith("skills/") and n.endswith("/SKILL.md") for n in names)
    assert ".claude-plugin/plugin.json" not in names  # pi ships no manifest


def test_opencode_zip_has_no_extensions_or_themes(dist):
    """Regression guard: pi's extras must not leak into the shared skills zip."""
    zip_path = build_mod.build_one("opencode", _common.load_version())
    names = _names(zip_path)

    assert not any(n.startswith(("extensions/", "themes/")) for n in names)
    # opencode ships flat skills (no skills/ prefix).
    assert any(n.endswith("/SKILL.md") for n in names)
    assert not any(n.startswith("skills/") for n in names)


def test_pi_install_layout_and_owned_only_cleanup(dist, tmp_path, monkeypatch):
    target_dir = tmp_path / "pi-agent"
    monkeypatch.setenv("ASSISTANT_PI_DIR", str(target_dir))

    assert install_mod.main(["pi"]) == 0
    assert (target_dir / "extensions" / "research.ts").is_file()
    assert (target_dir / "themes" / "dpurge-dark-default.json").is_file()
    assert any((target_dir / "skills").iterdir())

    # Plant the user's own unrelated content.
    mine_ext = target_dir / "extensions" / "mine.ts"
    mine_ext.write_text("// mine\n")
    mine_skill = target_dir / "skills" / "not-ours"
    mine_skill.mkdir()
    (mine_skill / "SKILL.md").write_text("x\n")

    # Reinstall replaces ours, preserves theirs.
    assert install_mod.main(["pi"]) == 0
    assert (target_dir / "extensions" / "research.ts").is_file()
    assert mine_ext.is_file()
    assert (mine_skill / "SKILL.md").is_file()

    # Uninstall removes only ours.
    assert uninstall_mod.main(["pi"]) == 0
    assert not (target_dir / "extensions" / "research.ts").exists()
    assert not (target_dir / "themes" / "dpurge-dark-default.json").exists()
    assert mine_ext.is_file()
    assert (mine_skill / "SKILL.md").is_file()
