"""Uninstall: remove this plugin's skills from the install directory.

Usage:
    uv run scripts/uninstall.py <claude|opencode|pi>

For `claude` the install directory is removed entirely (it is exclusive).
For `opencode` and `pi` only this plugin's skill subdirs are removed;
other (unrelated) skills sharing the directory are left alone.

Set ASSISTANT_FORCE=1 to remove a Claude install dir that does not look
like ours.
"""

from __future__ import annotations

import os
import shutil
import sys

from _common import (
    install_dir_for,
    installed_owned_skills,
    looks_like_claude_install,
    validate_target,
)


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        sys.stderr.write("usage: uninstall.py <claude|opencode|pi>\n")
        return 2

    target = argv[0]
    cfg = validate_target(target)
    install_dir = install_dir_for(target)
    force = bool(os.environ.get("ASSISTANT_FORCE"))

    if not install_dir.exists():
        print(f"nothing to uninstall: {install_dir} does not exist")
        return 0

    if cfg["shared_install_dir"]:
        removed = [p.name for p in installed_owned_skills(install_dir)]
        for p in installed_owned_skills(install_dir):
            shutil.rmtree(p)
        if removed:
            print(
                f"uninstalled assistant-{target}: removed "
                f"{len(removed)} skill(s) from {install_dir}"
            )
            for r in removed:
                print(f"  - {r}")
        else:
            print(
                f"nothing to uninstall: no owned skills found in {install_dir}"
            )
    else:
        if not looks_like_claude_install(install_dir) and not force:
            sys.stderr.write(
                f"refusing to remove {install_dir} — does not look like an assistant install\n"
                f"set ASSISTANT_FORCE=1 to override\n"
            )
            return 1
        shutil.rmtree(install_dir)
        print(f"uninstalled assistant-{target}: removed {install_dir}")

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
