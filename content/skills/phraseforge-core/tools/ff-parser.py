# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "pydantic>=2.6",
#   "pyyaml>=6.0",
# ]
# ///
"""Parse a *.ff PhraseForge source file and emit a Lesson JSON object.

A .ff file consists of a YAML header block followed by one or more named chunks
separated by === chunk-id === markers.  Each chunk is parsed according to the
document type declared in the header (vocabulary, model, text, or dialog).

Usage:
    uv run --script ff-parser.py path/to/source.ff
    uv run --script ff-parser.py path/to/source.ff --chunk 1
    uv run --script ff-parser.py path/to/source.ff --out lesson.json
    uv run --script ff-parser.py --print-schema

By default every chunk produces one Lesson JSON object written to stdout,
separated by a newline.  Use --chunk to emit only a single chunk (1-based).
Use --out to write to a file instead of stdout; with multiple chunks the output
is a JSON array.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Generator

import yaml
from pydantic import ValidationError

# ---------------------------------------------------------------------------
# lesson_schema — inlined so the tool is self-contained
# ---------------------------------------------------------------------------
# Dev-time: if running from the source tree, the canonical lesson_schema.py
# lives at content/_shared/. In an installed zip build.py injects a sibling
# copy next to this script, so sys.path[0] (script dir) finds it.
_HERE = Path(__file__).resolve().parent
_SHARED_DEV = _HERE.parent.parent.parent / "_shared"
if _SHARED_DEV.exists() and str(_SHARED_DEV) not in sys.path:
    sys.path.insert(0, str(_SHARED_DEV))

from lesson_schema import (  # noqa: E402
    DialogSource,
    DialogTurn,
    Lesson,
    ModelEntry,
    Narration,
    TextSource,
    VocabularyEntry,
)


# ---------------------------------------------------------------------------
# .ff file reader — produces (chunk_id, text) pairs
# ---------------------------------------------------------------------------

def _read_chunks(path: Path) -> Generator[tuple[str | None, str], None, None]:
    """Yield (chunk_id, body_text) pairs from a .ff file.

    The first pair always has chunk_id=None and contains the YAML header.
    Subsequent pairs correspond to === id === sections.
    """
    chunk_id: str | None = None
    buf: list[str] = []
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            stripped = line.strip()
            if stripped.startswith("===") and stripped.endswith("==="):
                yield chunk_id, "".join(buf).strip()
                chunk_id = stripped.strip("=").strip()
                buf = []
            else:
                buf.append(line)
    yield chunk_id, "".join(buf).strip()


# ---------------------------------------------------------------------------
# vocabulary body parser (adapted from phraseforge-data/lib/parser.py)
# ---------------------------------------------------------------------------

def _parse_grammar(text: str) -> str:
    return text.strip()


def _parse_vocabulary_line(line: str) -> VocabularyEntry | None:
    """Parse one vocabulary line into a VocabularyEntry.

    Format: headword {grammar} [transcription] = translation1; translation2 (note1; note2)
    All parts except the headword are optional.
    """
    line = line.strip()
    if not line:
        return None

    _phrase = line
    _grammar: str | None = None
    _transcription: str | None = None
    _translations_raw: str | None = None
    _notes: str | None = None

    # Split off everything to the right of the first '='
    eq = _phrase.find("=")
    if eq > -1:
        _translations_raw = _phrase[eq + 1:].strip()
        _phrase = _phrase[:eq].strip()

    # [transcription] — rightmost bracket pair on the headword side
    if _phrase.endswith("]"):
        j = _phrase.rfind("[")
        if j > -1:
            _transcription = _phrase[j + 1:-1].strip()
            _phrase = _phrase[:j].strip()

    # {grammar} — rightmost brace pair on the headword side
    if _phrase.endswith("}"):
        k = _phrase.rfind("{")
        if k > -1:
            _grammar = _parse_grammar(_phrase[k + 1:-1])
            _phrase = _phrase[:k].strip()

    # (notes) — trailing parenthetical on the translation side
    if _translations_raw and _translations_raw.endswith(")"):
        l = _translations_raw.rfind("(")
        if l > -1:
            _notes = "; ".join(n.strip() for n in _translations_raw[l + 1:-1].split(";"))
            _translations_raw = _translations_raw[:l].strip()

    translation: str | None = None
    if _translations_raw:
        parts = [t.strip() for t in _translations_raw.split(";") if t.strip()]
        translation = "; ".join(parts) if parts else None

    return VocabularyEntry(
        headword=_phrase,
        grammar=_grammar or None,
        transcription=_transcription,
        translation=translation,
        notes=_notes,
    )


def _parse_vocabulary(body: str) -> list[VocabularyEntry]:
    entries: list[VocabularyEntry] = []
    for line in body.splitlines():
        entry = _parse_vocabulary_line(line)
        if entry is not None:
            entries.append(entry)
    return entries


# ---------------------------------------------------------------------------
# model body parser
# ---------------------------------------------------------------------------

def _parse_model_line(line: str) -> ModelEntry | None:
    """Parse one model line into a ModelEntry.

    Format: pattern [transcription] = translation (notes)
    `translation` is required; all other optional parts follow the same
    bracket/brace conventions as vocabulary lines.
    """
    line = line.strip()
    if not line:
        return None

    _pattern = line
    _transcription: str | None = None
    _translation_raw: str | None = None
    _notes: str | None = None

    eq = _pattern.find("=")
    if eq > -1:
        _translation_raw = _pattern[eq + 1:].strip()
        _pattern = _pattern[:eq].strip()
    else:
        # Models without a translation are invalid — skip silently
        return None

    # [transcription]
    if _pattern.endswith("]"):
        j = _pattern.rfind("[")
        if j > -1:
            _transcription = _pattern[j + 1:-1].strip()
            _pattern = _pattern[:j].strip()

    # (notes) on the translation side
    if _translation_raw.endswith(")"):
        l = _translation_raw.rfind("(")
        if l > -1:
            _notes = "; ".join(n.strip() for n in _translation_raw[l + 1:-1].split(";"))
            _translation_raw = _translation_raw[:l].strip()

    translation = _translation_raw.strip() if _translation_raw else None
    if not translation:
        return None

    return ModelEntry(
        pattern=_pattern,
        translation=translation,
        transcription=_transcription,
        notes=_notes,
    )


def _parse_models(body: str) -> list[ModelEntry]:
    entries: list[ModelEntry] = []
    for line in body.splitlines():
        entry = _parse_model_line(line)
        if entry is not None:
            entries.append(entry)
    return entries


# ---------------------------------------------------------------------------
# dialog body parser
# ---------------------------------------------------------------------------

_SPEAKER_RE = re.compile(r"^@(.+):$")
_ANON_RE = re.compile(r"^--:$")
_INDENT_RE = re.compile(r"^(?:  |\t)")


def _parse_dialog(body: str) -> DialogSource:
    """Parse a raw dialog body into a structured DialogSource.

    Rules (mirrors phraseforge-web remark plugin conventions):
    - First non-blank line starting with '# ' → dialog title (consumed, not emitted as narration)
    - '@Speaker:' (non-indented) → start named DialogTurn
    - '--:' (non-indented) → start anonymous DialogTurn (speaker=None)
    - Lines indented with 2 spaces or a tab → body of the current turn
      - Blank indented line → paragraph separator within the turn
    - Non-indented non-blank line (not a speaker header) → Narration paragraph
    """
    lines = body.splitlines()
    title: str | None = None
    items: list[Narration | DialogTurn] = []

    # Current turn accumulator
    current_turn: DialogTurn | None = None
    current_para: list[str] = []

    def _flush_para() -> None:
        if current_turn is not None and current_para:
            text = " ".join(current_para).strip()
            if text:
                current_turn.paragraphs.append(text)
            current_para.clear()

    def _flush_turn() -> None:
        nonlocal current_turn
        _flush_para()
        if current_turn is not None:
            items.append(current_turn)
            current_turn = None

    # Skip leading blank lines; check for optional title
    i = 0
    while i < len(lines) and not lines[i].strip():
        i += 1
    if i < len(lines) and lines[i].startswith("# "):
        title = lines[i][2:].strip()
        i += 1

    for line in lines[i:]:
        stripped = line.strip()

        # Blank lines are paragraph separators inside a turn; elsewhere ignored.
        if not stripped:
            if current_turn is not None:
                _flush_para()
            continue

        m_speaker = _SPEAKER_RE.match(stripped)
        m_anon = _ANON_RE.match(stripped)

        if m_speaker or m_anon:
            _flush_turn()
            speaker = m_speaker.group(1).strip() if m_speaker else None
            current_turn = DialogTurn(speaker=speaker, paragraphs=[])
            continue

        if _INDENT_RE.match(line):
            # Indented non-blank line → turn body
            if current_turn is None:
                # Indented line before any turn header — treat as narration
                items.append(Narration(text=stripped))
                continue
            current_para.append(stripped)
            continue

        # Non-indented non-blank line: end any current turn, then narration
        _flush_turn()
        items.append(Narration(text=stripped))

    _flush_turn()

    return DialogSource(kind="dialog", title=title, items=items)


# ---------------------------------------------------------------------------
# .ff header → Lesson field extractor
# ---------------------------------------------------------------------------

def _parse_header(text: str) -> dict:
    """Parse the YAML header block of a .ff file into a flat dict."""
    data = yaml.safe_load(text) or {}
    lang: str = ""
    script: str = "latn"
    translation_lang: str | None = None
    translation_script: str | None = None

    data_block = data.get("data") or {}
    if isinstance(data_block, dict):
        lang = data_block.get("language", "")
        script = data_block.get("script", "latn")

    trans_block = data.get("translation") or {}
    if isinstance(trans_block, dict):
        translation_lang = trans_block.get("language") or None
        translation_script = trans_block.get("script") or None

    return {
        "title": data.get("document", ""),
        "description": data.get("description") or None,
        "doc_type": data.get("type", "vocabulary"),
        "lang": lang,
        "script": script,
        "translation_lang": translation_lang,
        "translation_script": translation_script,
    }


# ---------------------------------------------------------------------------
# chunk → Lesson
# ---------------------------------------------------------------------------

def _chunk_to_lesson(header: dict, chunk_id: str | None, body: str) -> Lesson:
    doc_type = header["doc_type"]

    vocabulary: list[VocabularyEntry] = []
    models: list[ModelEntry] = []
    source = None

    if doc_type == "vocabulary":
        vocabulary = _parse_vocabulary(body)
    elif doc_type == "model":
        models = _parse_models(body)
    elif doc_type == "dialog":
        source = _parse_dialog(body)
    elif doc_type == "text":
        source = TextSource(kind="text", content=body)

    title = header["title"]
    if chunk_id:
        title = f"{title} / {chunk_id}"

    return Lesson(
        title=title,
        description=header["description"],
        lang=header["lang"],
        script=header["script"],
        translation_lang=header["translation_lang"],
        translation_script=header["translation_script"],
        vocabulary=vocabulary,
        models=models,
        source=source,
    )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("input", nargs="?", default=None,
                   help="Path to a .ff source file")
    p.add_argument("--chunk", type=int, default=None,
                   help="Emit only this chunk (1-based index). Default: all chunks.")
    p.add_argument("--out", dest="output", default="-",
                   help="Output path; '-' for stdout (default)")
    p.add_argument("--print-schema", action="store_true",
                   help="Print the JSON Schema for the Lesson model and exit")
    args = p.parse_args()

    if args.print_schema:
        print(json.dumps(Lesson.model_json_schema(), indent=2, ensure_ascii=False))
        return 0

    if not args.input:
        p.print_usage(sys.stderr)
        sys.stderr.write("error: input file is required (use '-' for stdin)\n")
        return 1

    if args.input == "-":
        content = sys.stdin.read()
        import io
        lines_iter = iter(content.splitlines(keepends=True))

        def _read_chunks_from_string(text: str):
            chunk_id = None
            buf: list[str] = []
            for line in text.splitlines(keepends=True):
                stripped = line.strip()
                if stripped.startswith("===") and stripped.endswith("==="):
                    yield chunk_id, "".join(buf).strip()
                    chunk_id = stripped.strip("=").strip()
                    buf = []
                else:
                    buf.append(line)
            yield chunk_id, "".join(buf).strip()

        chunks_iter = _read_chunks_from_string(content)
    else:
        path = Path(args.input)
        if not path.exists():
            sys.stderr.write(f"error: file not found: {path}\n")
            return 1
        chunks_iter = _read_chunks(path)

    try:
        _, header_text = next(chunks_iter)
    except StopIteration:
        sys.stderr.write("error: empty file\n")
        return 1

    header = _parse_header(header_text)

    lessons: list[Lesson] = []
    chunk_index = 0
    for chunk_id, body in chunks_iter:
        chunk_index += 1
        if args.chunk is not None and chunk_index != args.chunk:
            continue
        try:
            lesson = _chunk_to_lesson(header, chunk_id, body)
        except ValidationError as e:
            sys.stderr.write(f"validation error in chunk {chunk_index!r}: {e}\n")
            return 1
        lessons.append(lesson)

    if not lessons:
        sys.stderr.write("warning: no chunks found (or --chunk index out of range)\n")
        return 0

    if args.chunk is not None or len(lessons) == 1:
        out_text = lessons[0].model_dump_json(indent=2, exclude_none=True)
    else:
        out_text = json.dumps(
            [json.loads(l.model_dump_json(exclude_none=True)) for l in lessons],
            indent=2,
            ensure_ascii=False,
        )

    if args.output == "-":
        sys.stdout.write(out_text)
        sys.stdout.write("\n")
    else:
        Path(args.output).write_text(out_text + "\n", encoding="utf-8")
        sys.stderr.write(f"wrote {args.output}\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
