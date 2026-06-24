# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "pydantic>=2.6",
#   "jinja2>=3.1",
# ]
# ///
"""Render a phraseforge lesson JSON as a Docusaurus MDX file for phraseforge-web.

Usage:
    uv run --script mdx-export.py [--in lesson.json] [--out lesson.mdx]
    uv run --script mdx-export.py --print-schema    # dump JSON Schema, exit

Validation: input JSON is parsed against the Lesson model in `lesson_schema.py`.
Bad inputs exit 1 with a path-aware Pydantic ValidationError on stderr.

Output: a Docusaurus MDX file matching the phraseforge-web parser conventions —
YAML frontmatter, H1 title, `vocabulary` / `models` code fences with
`<headword> {grammar} [transcription] = translation` syntax, `<Text>` JSX or
`dialog` code fence (with `@Speaker:` / `--:` headers) for source, optional
transcription/translation `<Text>` mirror blocks, `<Questions>` ordered list,
and one `<Exercise>` per entry.

Drop the output under `docs/<lang3>/<level>/<YYYY-MM-DD>-<seq>.mdx` of a
phraseforge-web clone.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Dev-time: if running from the source tree, the canonical `lesson_schema.py`
# lives at content/_shared/. In an installed zip, build.py injects a sibling
# copy next to this script, so sys.path[0] (script dir) finds it.
_HERE = Path(__file__).resolve().parent
_SHARED_DEV = _HERE.parent.parent.parent / "_shared"
if _SHARED_DEV.exists() and str(_SHARED_DEV) not in sys.path:
    sys.path.insert(0, str(_SHARED_DEV))

from jinja2 import Environment, FileSystemLoader, StrictUndefined  # noqa: E402
from lesson_schema import DialogTurn, Lesson, Narration  # noqa: E402
from pydantic import ValidationError  # noqa: E402

HERE = _HERE
TEMPLATES_DIR = HERE / "templates"


def _format_dialog_body(items) -> str:
    """Render the body of a phraseforge-web `dialog` code fence.

    Per dialog.md: narration is non-indented prose; turns have a `@Speaker:`
    or `--:` header followed by 2-space-indented body lines; paragraphs
    within a turn are separated by a blank line; blank line between items.
    """
    out: list[str] = []
    for item in items:
        if isinstance(item, Narration):
            if not item.text:
                continue
            out.append("")
            out.append(item.text)
        elif isinstance(item, DialogTurn):
            body = [p for p in item.paragraphs if p]
            if not body:
                continue
            out.append("")
            out.append(f"@{item.speaker}:" if item.speaker else "--:")
            for i, para in enumerate(body):
                out.append(f"  {para}")
                if i < len(body) - 1:
                    out.append("")
    return "\n".join(out)


def _yaml_string(value) -> str:
    """Render a value as a safe YAML scalar string.

    JSON strings are a strict subset of YAML strings, so `json.dumps(s)`
    produces a YAML-valid double-quoted string with all the right escapes.
    """
    if value is None:
        return "null"
    return json.dumps(str(value), ensure_ascii=False)


def _env() -> Environment:
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        undefined=StrictUndefined,
        autoescape=False,
        keep_trailing_newline=True,
    )
    env.filters["yaml_string"] = _yaml_string
    return env


def render(lesson: Lesson) -> str:
    dialog_body = ""
    if lesson.source and lesson.source.kind == "dialog":
        dialog_body = _format_dialog_body(lesson.source.items)
    dialog_translation_body = ""
    if lesson.translation_dialog and lesson.translation_dialog.items:
        dialog_translation_body = _format_dialog_body(lesson.translation_dialog.items)
    template = _env().get_template("lesson.mdx.j2")
    return template.render(
        lesson=lesson,
        dialog_body=dialog_body,
        dialog_translation_body=dialog_translation_body,
    )


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--in", dest="input", default="-",
                   help="JSON input path; '-' for stdin (default)")
    p.add_argument("--out", dest="output", default="-",
                   help="Output .mdx path; '-' for stdout (default)")
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

    out = render(lesson)

    if args.output == "-":
        sys.stdout.write(out)
    else:
        Path(args.output).write_text(out, encoding="utf-8")
        sys.stderr.write(f"wrote {args.output}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
