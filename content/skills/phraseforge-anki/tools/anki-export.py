# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "pydantic>=2.6",
#   "jinja2>=3.1",
# ]
# ///
"""Render phraseforge lesson vocabulary as a TSV file targeting the
dpurge/anki-flashcards repo (https://github.com/dpurge/anki-flashcards).

Usage:
    uv run --script anki-export.py [--in lesson.json] [--out cards.csv] [--source SLUG]
    uv run --script anki-export.py --print-schema   # dump JSON Schema, exit

Validation: input JSON is parsed against the Lesson model in `lesson_schema.py`.
Bad inputs exit 1 with a path-aware Pydantic ValidationError on stderr.

Output: tab-separated rows with the upstream header
    Phrase\\tGrammar\\tTranscription\\tTranslation\\tNotes
followed by a `# === <slug> ===` section marker and one row per vocab entry.
Drop the file under `dat/lang-vocabulary/<lang>/` of an anki-flashcards clone,
register it in that directory's `flashcard.yml` `data:` block, then run
`task clean build` to produce `.apkg`s.
"""

from __future__ import annotations

import argparse
import json
import sys
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


def _tsv_safe(value) -> str:
    """Strip and collapse separators that would break TSV row parsing."""
    if value is None:
        return ""
    return (
        str(value)
        .replace("\t", " ")
        .replace("\n", " ")
        .replace("\r", " ")
        .strip()
    )


def _env() -> Environment:
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        undefined=StrictUndefined,
        autoescape=False,
        keep_trailing_newline=True,
    )
    env.filters["tsv_safe"] = _tsv_safe
    return env


def _derive_slug(lesson: Lesson, override: str | None) -> str:
    if override:
        return override
    date = (lesson.date or "").strip()
    title = (lesson.title or "").strip()
    if date and title:
        return f"{date} {title}"
    return date or title or "phraseforge"


def render(lesson: Lesson, source_slug: str | None) -> str:
    rows: list[list[str]] = []
    for entry in lesson.vocabulary:
        phrase = _tsv_safe(entry.headword)
        if not phrase:
            # Skip entries without a phrase — Phrase is indexed; Anki rejects empties.
            continue
        rows.append([
            phrase,
            _tsv_safe(entry.grammar),
            _tsv_safe(entry.transcription),
            _tsv_safe(entry.translation),
            _tsv_safe(entry.notes),
        ])

    template = _env().get_template("cards.tsv.j2")
    return template.render(
        slug=_derive_slug(lesson, source_slug),
        rows=rows,
    )


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--in", dest="input", default="-",
                   help="JSON input path; '-' for stdin (default)")
    p.add_argument("--out", dest="output", default="-",
                   help="TSV output path; '-' for stdout (default)")
    p.add_argument("--source", default=None,
                   help="Override the `# === <slug> ===` section marker")
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

    if not lesson.vocabulary:
        sys.stderr.write("warning: input has no `vocabulary` field; output will contain only the header\n")

    out = render(lesson, args.source)

    if args.output == "-":
        sys.stdout.write(out)
    else:
        Path(args.output).write_text(out, encoding="utf-8")
        sys.stderr.write(f"wrote {args.output}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
