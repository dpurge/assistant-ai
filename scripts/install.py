# /// script
# requires-python = ">=3.11"
# ///
"""Install: build the target zip then unpack it into the install directory.

Usage:
    uv run scripts/install.py <claude|opencode|pi>

Environment:
    ASSISTANT_{CLAUDE,OPENCODE,PI}_DIR  override the install destination
    ASSISTANT_FORCE=1                   overwrite a non-empty, unrelated dir
                                        (claude only)

For `claude` the install directory is exclusive — wiped before unpack.
For `opencode` and `pi` the install directory is shared with other skills;
only this plugin's skills are touched.
"""

from __future__ import annotations

import os
import sys
import zipfile

import build as build_mod
from _common import (
    install_dir_for,
    load_version,
    looks_like_claude_install,
    owned_install_paths,
    rmtree,
    validate_target,
    zip_path_for,
)


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        sys.stderr.write("usage: install.py <claude|opencode|pi>\n")
        return 2

    target = argv[0]
    cfg = validate_target(target)
    version = load_version()
    install_dir = install_dir_for(target)
    force = bool(os.environ.get("ASSISTANT_FORCE"))

    if cfg["shared_install_dir"]:
        # opencode / pi: leave the user's unrelated content alone; replace ours
        # (owned skill dirs + owned extension/theme files).
        for our in owned_install_paths(target, install_dir):
            rmtree(our) if our.is_dir() else our.unlink()
    else:
        # claude: exclusive dir.
        if install_dir.exists() and any(install_dir.iterdir()):
            if looks_like_claude_install(install_dir) or force:
                rmtree(install_dir)
            else:
                sys.stderr.write(
                    f"refusing to install into non-empty, unrelated dir {install_dir}\n"
                    f"set ASSISTANT_FORCE=1 to override\n"
                )
                return 1

    build_mod.build_one(target, version)

    install_dir.mkdir(parents=True, exist_ok=True)
    zip_path = zip_path_for(target, version)
    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(install_dir)
    print(f"installed assistant-{target} v{version} -> {install_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
