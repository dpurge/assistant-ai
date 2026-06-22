"""Bump the version in plugins/claude/.claude-plugin/plugin.json.

Usage:
    uv run scripts/bump_version.py <new-version>

Accepts the new version with or without a leading `v`. Validates semver
shape (major.minor.patch with optional `-pre` suffix), rewrites the
manifest in place, and prints the git commands to commit, tag, and push
the release.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST = REPO_ROOT / "plugins" / "claude" / ".claude-plugin" / "plugin.json"

SEMVER = re.compile(r"^\d+\.\d+\.\d+(?:-[A-Za-z0-9.-]+)?$")


def main() -> int:
    if len(sys.argv) != 2:
        sys.stderr.write("usage: bump_version.py <new-version>\n")
        return 2

    new = sys.argv[1].lstrip("v")
    if not SEMVER.match(new):
        sys.stderr.write(
            f"not a valid semver: {new!r}\n"
            "expected major.minor.patch (optionally with -prerelease)\n"
        )
        return 1

    with MANIFEST.open("r", encoding="utf-8") as f:
        data = json.load(f)

    old = data.get("version", "?")
    if old == new:
        sys.stderr.write(f"version is already {new}; nothing to do\n")
        return 0

    data["version"] = new
    with MANIFEST.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"bumped {MANIFEST.relative_to(REPO_ROOT)}: {old} -> {new}")
    print()
    print("Next steps:")
    print(f"  git add {MANIFEST.relative_to(REPO_ROOT)}")
    print(f'  git commit -m "release: v{new}"')
    print(f"  git tag v{new}")
    print(f"  git push origin main")
    print(f"  git push origin v{new}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
