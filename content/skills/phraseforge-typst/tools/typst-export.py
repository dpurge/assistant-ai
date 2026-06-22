# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "pydantic>=2.6",
#   "jinja2>=3.1",
# ]
# ///
"""Render a phraseforge lesson JSON as a Typst (.typ) source.

Usage:
    uv run --script typst-export.py [--in lesson.json] [--out lesson.typ] \
                                    [--package-version 0.0.1]
    uv run --script typst-export.py --print-schema   # dump JSON Schema, exit

Validation: input JSON is parsed against the Lesson model in `lesson_schema.py`.
Bad inputs exit 1 with a path-aware Pydantic ValidationError on stderr.

Output: a Typst document that imports `@local/dpurge-langnote:<package-version>`.
Compile with `typst compile <out> <out>.pdf` once the dpurge-langnote package
is installed in your Typst local-packages directory.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

# Dev-time: if running from the source tree, the canonical `lesson_schema.py`
# lives at content/_shared/. In an installed zip, build.py injects a sibling
# copy next to this script, so sys.path[0] (script dir) finds it. The check
# below adds the shared dir only if the dev-tree layout is present.
_HERE = Path(__file__).resolve().parent
_SHARED_DEV = _HERE.parent.parent.parent / "_shared"
if _SHARED_DEV.exists() and str(_SHARED_DEV) not in sys.path:
    sys.path.insert(0, str(_SHARED_DEV))

from jinja2 import Environment, FileSystemLoader, StrictUndefined  # noqa: E402
from lesson_schema import Lesson  # noqa: E402
from pydantic import ValidationError  # noqa: E402

HERE = _HERE
TEMPLATES_DIR = HERE / "templates"


# --- escape helpers (Jinja2 filters) -----------------------------------------

def _content_escape(value) -> str:
    """Escape text for use inside a Typst content block `[ ... ]`.

    Escapes: `\\`, `#`, `[`, `]`. Other special chars (`*`, `_`, `$`) are not
    escaped — they are only meaningful with specific delimiter patterns and
    safe as literals in plain prose.
    """
    if value is None:
        return ""
    s = str(value)
    return (
        s.replace("\\", "\\\\")
         .replace("#", "\\#")
         .replace("[", "\\[")
         .replace("]", "\\]")
    )


def _string_literal(value) -> str:
    """Render a value as a Typst double-quoted string literal."""
    if value is None:
        return "none"
    body = str(value).replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
    return f'"{body}"'


# --- core --------------------------------------------------------------------

def _env() -> Environment:
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        undefined=StrictUndefined,
        autoescape=False,
        keep_trailing_newline=True,
    )
    env.filters["content_escape"] = _content_escape
    env.filters["string_literal"] = _string_literal
    return env


def render(lesson: Lesson, package_version: str) -> str:
    # Resolve date components; fall back to today if missing or unparseable.
    try:
        d = date.fromisoformat(lesson.date) if lesson.date else date.today()
    except (TypeError, ValueError):
        d = date.today()

    # Pass the Pydantic model itself (not model_dump): attribute access on
    # dicts can collide with built-in dict methods (e.g. `ex.items` would
    # resolve to dict.items, not the field). Pydantic models expose fields as
    # attributes, so this is safe.
    template = _env().get_template("lesson.typ.j2")
    return template.render(
        lesson=lesson,
        package_version=package_version,
        date_year=d.year,
        date_month=d.month,
        date_day=d.day,
    )


# --- CLI ---------------------------------------------------------------------

def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--in", dest="input", default="-",
                   help="JSON input path; '-' for stdin (default)")
    p.add_argument("--out", dest="output", default="-",
                   help="Output .typ path; '-' for stdout (default)")
    p.add_argument("--package-version", default="0.0.1",
                   help="dpurge-langnote version to import (default: 0.0.1)")
    p.add_argument("--print-schema", action="store_true",
                   help="Print the JSON Schema for the input contract and exit")
    args = p.parse_args()

    if args.print_schema:
        print(json.dumps(Lesson.model_json_schema(), indent=2, ensure_ascii=False))
        return 0

    raw = sys.stdin.read() if args.input == "-" else Path(args.input).read_text(encoding="utf-8")

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        sys.stderr.write(f"invalid JSON: {e}\n")
        return 1

    try:
        lesson = Lesson.model_validate(data)
    except ValidationError as e:
        sys.stderr.write(f"{e}\n")
        return 1

    out = render(lesson, args.package_version)

    if args.output == "-":
        sys.stdout.write(out)
    else:
        Path(args.output).write_text(out, encoding="utf-8")
        sys.stderr.write(f"wrote {args.output}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
