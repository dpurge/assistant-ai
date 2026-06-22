"""Shared helpers and constants for the assistant-ai build/install scripts."""

from __future__ import annotations

import functools
import json
import os
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
        "default_dir": "~/.pi/agent/skills",
        "env": "ASSISTANT_PI_DIR",
        "include_manifest": False,
        "skills_zip_prefix": "",
        "shared_install_dir": True,
        "zip_artifact": "skills",
    },
}

# Map: skill folder name → list of file names under content/_shared/ to inject
# next to that skill's tools/ at build time. Lets multiple skills share a single
# canonical source file without symlinks or runtime imports across skills.
SHARED_BY_SKILL: dict[str, list[str]] = {
    "phraseforge-typst": ["lesson_schema.py"],
    "phraseforge-anki": ["lesson_schema.py"],
    "phraseforge-web": ["lesson_schema.py"],
}


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


def installed_owned_skills(install_dir: Path) -> list[Path]:
    """List owned skill subdirs currently present under install_dir."""
    if not install_dir.exists():
        return []
    return sorted(p for p in install_dir.iterdir() if is_owned_skill_dir(p))


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
