# /// script
# requires-python = ">=3.11"
# ///
"""Remove the dist/ build-output directory."""

from __future__ import annotations

import sys

from _common import DIST_DIR, rmtree


def main() -> int:
    if DIST_DIR.exists():
        rmtree(DIST_DIR)
        print(f"removed {DIST_DIR}")
    else:
        print(f"nothing to clean ({DIST_DIR} does not exist)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
