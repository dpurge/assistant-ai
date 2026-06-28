# /// script
# requires-python = ">=3.11"
# ///
"""Build distributable zip archives for one or all assistant-ai targets.

Usage:
    uv run scripts/build.py              # build all targets
    uv run scripts/build.py claude       # build only the claude target
    uv run scripts/build.py claude pi    # build claude and pi
"""

from __future__ import annotations

import sys
import zipfile

from _common import (
    CLAUDE_MANIFEST,
    DIST_DIR,
    REPO_ROOT,
    SHARED_BY_SKILL,
    SHARED_DIR,
    TARGETS,
    discover_skills,
    load_version,
    skip_file as _skip_file,
    validate_target,
    zip_path_for,
)


def build_one(target: str, version: str):
    """Build the zip artifact for `target` if it doesn't already exist on disk.

    Multiple targets can share a zip_artifact and therefore the same file —
    when called for a second target with the same artifact, this returns the
    existing zip without rebuilding.
    """
    cfg = TARGETS[target]
    zip_path = zip_path_for(target, version)
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    if zip_path.exists():
        # Already built this run; nothing to do.
        return zip_path

    skills_prefix = cfg["skills_zip_prefix"]
    skills = discover_skills()

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        if cfg["include_manifest"]:
            z.write(CLAUDE_MANIFEST, arcname=".claude-plugin/plugin.json")

        for skill_dir in skills:
            # Skill's own files
            for f in sorted(skill_dir.rglob("*")):
                if not f.is_file() or _skip_file(f):
                    continue
                rel = f.relative_to(skill_dir).as_posix()
                arc = f"{skills_prefix}{skill_dir.name}/{rel}"
                z.write(f, arcname=arc)
            # Injected shared files (next to the skill's tools/)
            for shared_name in SHARED_BY_SKILL.get(skill_dir.name, []):
                src = SHARED_DIR / shared_name
                if not src.exists():
                    sys.stderr.write(f"warning: shared file missing: {src}\n")
                    continue
                arc = f"{skills_prefix}{skill_dir.name}/tools/{shared_name}"
                z.write(src, arcname=arc)

        # Non-skill content (e.g. Pi extensions/themes), shipped verbatim.
        extra_count = 0
        for entry in cfg.get("extra_content", []):
            src_root = REPO_ROOT / entry["src"]
            if not src_root.exists():
                sys.stderr.write(f"warning: extra content missing: {src_root}\n")
                continue
            for f in sorted(src_root.rglob("*")):
                if not f.is_file() or _skip_file(f):
                    continue
                rel = f.relative_to(src_root).as_posix()
                z.write(f, arcname=f"{entry['arc_prefix']}{rel}")
                extra_count += 1

    size = zip_path.stat().st_size
    extra = f", {extra_count} extra file(s)" if extra_count else ""
    print(
        f"built dist/{zip_path.name} ({size:,} bytes, {len(skills)} skill(s){extra})"
    )
    return zip_path


def main(argv: list[str]) -> int:
    version = load_version()
    if argv:
        for t in argv:
            validate_target(t)
        targets = argv
    else:
        targets = list(TARGETS)
    # Dedupe targets by zip_artifact — same artifact, same zip, build once.
    seen_artifacts: set[str] = set()
    for t in targets:
        artifact = TARGETS[t]["zip_artifact"]
        if artifact in seen_artifacts:
            continue
        seen_artifacts.add(artifact)
        build_one(t, version)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
