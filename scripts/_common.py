"""Shared helpers and constants for the assistant-ai build/install scripts."""

from __future__ import annotations

import functools
import json
import os
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = REPO_ROOT / "content"
SKILLS_ROOT = CONTENT_DIR / "skills"
SHARED_DIR = CONTENT_DIR / "_shared"
CLAUDE_MANIFEST = REPO_ROOT / "plugins" / "claude" / ".claude-plugin" / "plugin.json"
DIST_DIR = REPO_ROOT / "dist"

# `zip_artifact` controls the dist/ filename suffix. Targets with the same
# zip_artifact share a single zip file (built once per build invocation).
TARGETS = {
    "claude": {
        # Exclusive install dir: the plugin is the sole occupant.
        "default_dir": "~/.claude/plugins/assistant",
        "env": "ASSISTANT_CLAUDE_DIR",
        "include_manifest": True,
        "skills_zip_prefix": "skills/",
        "shared_install_dir": False,
        "zip_artifact": "claude",
    },
    "opencode": {
        # Shared install dir: unrelated skills may also live here.
        # Original archived opencode-ai/opencode; default path is best-guess —
        # verify with `ls ~/.config/opencode/` on your machine.
        "default_dir": "~/.config/opencode/skills",
        "env": "ASSISTANT_OPENCODE_DIR",
        "include_manifest": False,
        "skills_zip_prefix": "",
        "shared_install_dir": True,
        "zip_artifact": "skills",
    },
    "pi": {
        # Self-contained bundle unpacked into the Pi agent base dir. The dir is
        # shared (skills/, extensions/, themes/, settings.json may hold the
        # user's own content), so only owned files are touched on (un)install.
        # NOTE: ASSISTANT_PI_DIR now points at the base dir, not the skills dir.
        "default_dir": "~/.pi/agent",
        "env": "ASSISTANT_PI_DIR",
        "include_manifest": False,
        "skills_zip_prefix": "skills/",
        "shared_install_dir": True,
        "zip_artifact": "pi",
        # Non-skill content roots (repo-relative src → arcname prefix). Pi loads
        # extensions from extensions/*.ts (jiti, no build) and themes from
        # themes/*.json.
        "extra_content": [
            {"src": "plugins/pi/extensions", "arc_prefix": "extensions/"},
            {"src": "plugins/pi/themes", "arc_prefix": "themes/"},
        ],
    },
}

# Map: skill folder name → list of file names under content/_shared/ to inject
# next to that skill's tools/ at build time. Lets multiple skills share a single
# canonical source file without symlinks or runtime imports across skills.
SHARED_BY_SKILL: dict[str, list[str]] = {
    "phraseforge-core": ["lesson_schema.py"],
    "phraseforge-typst": ["lesson_schema.py"],
    "phraseforge-anki": ["lesson_schema.py"],
    "phraseforge-web": ["lesson_schema.py"],
}


def skip_file(p: Path) -> bool:
    """Files we never want to ship in a zip or treat as owned content."""
    name = p.name
    if name.endswith(".pyc"):
        return True
    if "__pycache__" in p.parts:
        return True
    if name == ".DS_Store":
        return True
    return False


def rmtree(path: Path) -> None:
    """shutil.rmtree that clears read-only bits before deletion (required on Windows)."""
    import stat

    def _on_error(func, p, exc_info):
        os.chmod(p, stat.S_IWRITE)
        func(p)

    shutil.rmtree(path, onerror=_on_error)


def load_version() -> str:
    with CLAUDE_MANIFEST.open("r", encoding="utf-8") as f:
        return json.load(f)["version"]


def validate_target(target: str) -> dict:
    if target not in TARGETS:
        sys.stderr.write(
            f"unknown target {target!r}; valid: {', '.join(TARGETS)}\n"
        )
        sys.exit(2)
    return TARGETS[target]


def install_dir_for(target: str) -> Path:
    cfg = TARGETS[target]
    override = os.environ.get(cfg["env"])
    raw = override if override else cfg["default_dir"]
    return Path(raw).expanduser()


def zip_path_for(target: str, version: str) -> Path:
    """Path of the zip artifact backing this target.

    Targets sharing a `zip_artifact` value resolve to the same file — built
    once per build invocation, unpacked into different install directories.
    """
    artifact = TARGETS[target]["zip_artifact"]
    return DIST_DIR / f"assistant-{artifact}-{version}.zip"


def discover_skills() -> list[Path]:
    """Return all skill directories under content/skills/, sorted by name."""
    return sorted(
        p for p in SKILLS_ROOT.iterdir()
        if p.is_dir() and (p / "SKILL.md").exists()
    )


@functools.lru_cache(maxsize=1)
def owned_skill_names() -> frozenset[str]:
    """Skill folder names this plugin ships, derived from content/skills/."""
    return frozenset(p.name for p in discover_skills())


def is_owned_skill_dir(p: Path) -> bool:
    """True if p is a skill we ship, currently installed (has SKILL.md)."""
    return p.is_dir() and p.name in owned_skill_names() and (p / "SKILL.md").exists()


def installed_owned_skills(skills_root: Path) -> list[Path]:
    """List owned skill subdirs currently present directly under skills_root."""
    if not skills_root.exists():
        return []
    return sorted(p for p in skills_root.iterdir() if is_owned_skill_dir(p))


def skills_install_root(target: str, install_dir: Path) -> Path:
    """Dir that holds skill subdirs for this target.

    Equals install_dir for targets with an empty skills_zip_prefix (opencode);
    install_dir/skills for targets that nest skills under a prefix (pi).
    """
    prefix = TARGETS[target]["skills_zip_prefix"].rstrip("/")
    return install_dir / prefix if prefix else install_dir


def owned_files_under(src_root: Path) -> list[str]:
    """Relative posix paths of all shippable files under a repo-relative src dir."""
    if not src_root.exists():
        return []
    return sorted(
        f.relative_to(src_root).as_posix()
        for f in src_root.rglob("*")
        if f.is_file() and not skip_file(f)
    )


def owned_install_paths(target: str, install_dir: Path) -> list[Path]:
    """Existing install paths owned by this plugin for a shared-dir target.

    Single source of truth for install/uninstall cleanup: owned skill dirs plus
    each owned extension/theme file. Never includes the user's unrelated content.
    """
    cfg = TARGETS[target]
    paths: list[Path] = list(installed_owned_skills(skills_install_root(target, install_dir)))
    for entry in cfg.get("extra_content", []):
        base = install_dir / entry["arc_prefix"].rstrip("/")
        for rel in owned_files_under(REPO_ROOT / entry["src"]):
            p = base / rel
            if p.exists():
                paths.append(p)
    return paths


def looks_like_claude_install(p: Path) -> bool:
    """True if p is a Claude plugin dir we previously installed."""
    if (p / ".claude-plugin" / "plugin.json").exists():
        return True
    skills_dir = p / "skills"
    if skills_dir.exists():
        owned = owned_skill_names()
        if any((skills_dir / name / "SKILL.md").exists() for name in owned):
            return True
    return False
