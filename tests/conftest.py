"""Shared paths and helpers for the assistant-ai test suite."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
FIXTURES = Path(__file__).resolve().parent / "fixtures"
GOLDEN = Path(__file__).resolve().parent / "golden"

TYPST_TOOL = REPO_ROOT / "content" / "skills" / "phraseforge-typst" / "tools" / "typst-export.py"
ANKI_TOOL = REPO_ROOT / "content" / "skills" / "phraseforge-anki" / "tools" / "anki-export.py"
MDX_TOOL = REPO_ROOT / "content" / "skills" / "phraseforge-web" / "tools" / "mdx-export.py"


def run_tool(tool: Path, *args: str, stdin: str | None = None) -> subprocess.CompletedProcess:
    """Invoke a tool via `uv run --script` and capture stdout, stderr, returncode."""
    cmd = ["uv", "run", "--script", str(tool), *args]
    return subprocess.run(
        cmd,
        input=stdin,
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
        timeout=60,
    )
