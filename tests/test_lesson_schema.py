"""Unit tests for the shared Pydantic Lesson model.

Imports the canonical schema from `content/_shared/lesson_schema.py`.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SHARED = REPO_ROOT / "content" / "_shared"
sys.path.insert(0, str(SHARED))

from lesson_schema import (  # noqa: E402
    DialogSource,
    DialogTurn,
    Lesson,
    ModelEntry,
    Narration,
    TextSource,
    VocabularyEntry,
)
from pydantic import ValidationError  # noqa: E402


def test_minimal_lesson_has_defaults():
    lesson = Lesson(title="x", lang="lat")
    assert lesson.script == "latn"
    assert lesson.version == 1
    assert lesson.vocabulary == []
    assert lesson.models == []
    assert lesson.exercises == []
    assert lesson.grammar is None


def test_grammar_field_accepts_markdown():
    lesson = Lesson(title="x", lang="lat", grammar="## Gramatyka\n\ntreść")
    assert lesson.grammar.startswith("## Gramatyka")


def test_missing_title_fails():
    with pytest.raises(ValidationError) as exc:
        Lesson(lang="lat")
    assert "title" in str(exc.value)


def test_missing_lang_fails():
    with pytest.raises(ValidationError) as exc:
        Lesson(title="x")
    assert "lang" in str(exc.value)


def test_model_entry_requires_translation():
    """Bare strings no longer accepted; translation is required on every entry."""
    with pytest.raises(ValidationError) as exc:
        Lesson.model_validate({
            "title": "x",
            "lang": "lat",
            "models": ["plain string"],
        })
    # The bare string can't supply a translation field.
    assert "model" in str(exc.value).lower() or "translation" in str(exc.value).lower()


def test_model_entry_translation_required_in_dict_form():
    with pytest.raises(ValidationError) as exc:
        Lesson.model_validate({
            "title": "x",
            "lang": "lat",
            "models": [{"pattern": "phrase"}],
        })
    msg = str(exc.value)
    assert "translation" in msg
    assert "missing" in msg.lower() or "Field required" in msg


def test_full_model_entry():
    lesson = Lesson.model_validate({
        "title": "x",
        "lang": "lat",
        "models": [
            {"pattern": "phrase", "translation": "fraza"},
            {"pattern": "another", "translation": "kolejna", "transcription": "roman"},
        ],
    })
    assert lesson.models[0].pattern == "phrase"
    assert lesson.models[0].translation == "fraza"
    assert lesson.models[0].transcription is None
    assert lesson.models[1].transcription == "roman"


def test_text_source_dispatch():
    lesson = Lesson.model_validate({
        "title": "x", "lang": "lat",
        "source": {"kind": "text", "content": "hello"},
    })
    assert isinstance(lesson.source, TextSource)
    assert lesson.source.content == "hello"


def test_dialog_source_dispatch():
    lesson = Lesson.model_validate({
        "title": "x", "lang": "lat",
        "source": {
            "kind": "dialog",
            "title": "A chat",
            "items": [
                {"kind": "turn", "speaker": "A", "paragraphs": ["Hi", "How are you?"]},
            ],
        },
    })
    assert isinstance(lesson.source, DialogSource)
    assert lesson.source.title == "A chat"
    assert len(lesson.source.items) == 1
    turn = lesson.source.items[0]
    assert isinstance(turn, DialogTurn)
    assert turn.speaker == "A"
    assert turn.paragraphs == ["Hi", "How are you?"]


def test_dialog_narration_and_anonymous():
    lesson = Lesson.model_validate({
        "title": "x", "lang": "lat",
        "source": {
            "kind": "dialog",
            "items": [
                {"kind": "narration", "text": "Setting the scene."},
                {"kind": "turn", "speaker": None, "paragraphs": ["Anonymous voice."]},
                {"kind": "turn", "speaker": "B", "paragraphs": ["Hello."]},
            ],
        },
    })
    assert isinstance(lesson.source.items[0], Narration)
    assert lesson.source.items[0].text == "Setting the scene."
    assert isinstance(lesson.source.items[1], DialogTurn)
    assert lesson.source.items[1].speaker is None
    assert isinstance(lesson.source.items[2], DialogTurn)


def test_bad_source_kind_fails():
    with pytest.raises(ValidationError) as exc:
        Lesson.model_validate({
            "title": "x", "lang": "lat",
            "source": {"kind": "poem", "content": "x"},
        })
    msg = str(exc.value)
    assert "source" in msg
    assert "text" in msg and "dialog" in msg


def test_vocabulary_required_headword():
    with pytest.raises(ValidationError):
        VocabularyEntry()


def test_vocabulary_optional_fields():
    e = VocabularyEntry(headword="der Hund")
    assert e.grammar is None
    assert e.translation is None
