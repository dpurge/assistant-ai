"""Pydantic models for the phraseforge lesson JSON contract.

This file is duplicated across:
    content/skills/phraseforge-typst/tools/lesson_schema.py
    content/skills/phraseforge-anki/tools/lesson_schema.py

Keep them byte-identical. The wire-format spec lives in
`<skill>/references/lesson.schema.json`, generated via
`uv run --script <tool>.py --print-schema`.
"""

from __future__ import annotations

from typing import Annotated, Literal

from pydantic import BaseModel, Field


class VocabularyEntry(BaseModel):
    headword: str
    grammar: str | None = None
    transcription: str | None = None
    translation: str | None = Field(
        None,
        description=(
            "Polish gloss. Separate multiple senses with '; ' (semicolon + space) — "
            "e.g. 'wszyscy; wszystkie', 'dzień dobry; cześć'."
        ),
    )
    notes: str | None = None


class ModelEntry(BaseModel):
    """A model / phrase pattern.

    `pattern` is the foreign phrase. `translation` (required) is its Polish
    gloss; multiple senses separated by '; '. `transcription` is the romanized
    form, used for non-Latin scripts. `notes` carries optional usage notes,
    multiple notes joined with '; '.
    """
    pattern: str
    translation: str = Field(..., description="Polish gloss for the pattern. Required.")
    transcription: str | None = None
    notes: str | None = None


class TextSource(BaseModel):
    kind: Literal["text"] = "text"
    content: str


class Narration(BaseModel):
    """A non-speaker prose paragraph between turns in a dialog.

    Stage directions, scene-setting, off-screen voices, etc. In the surrounding
    dialog's language (e.g. Polish prose around a Polish dialog).
    """
    kind: Literal["narration"] = "narration"
    text: str


class DialogTurn(BaseModel):
    """A speaker turn within a dialog.

    `speaker` None marks an anonymous turn (`--:` in phraseforge-web's MDX,
    em-dash in renderers). `paragraphs` is the body — each entry is one
    paragraph; multiple entries render as separate paragraphs.
    """
    kind: Literal["turn"] = "turn"
    speaker: str | None = None
    paragraphs: list[str] = Field(default_factory=list)


DialogItem = Annotated[Narration | DialogTurn, Field(discriminator="kind")]


class DialogSource(BaseModel):
    """A dialog source. Matches the phraseforge-web `dialog` code-fence parser
    model: optional title, interleaved narration paragraphs and speaker turns,
    each turn optionally anonymous and optionally multi-paragraph.
    """
    kind: Literal["dialog"]
    title: str | None = None
    items: list[DialogItem] = Field(default_factory=list)


class Exercise(BaseModel):
    type: str
    instruction: str | None = None
    items: list[str] = Field(default_factory=list)


Source = Annotated[TextSource | DialogSource, Field(discriminator="kind")]


class Lesson(BaseModel):
    version: int = 1
    title: str
    description: str | None = None
    lang: str = Field(..., description="ISO 639-3 code of the foreign language")
    script: str = Field("latn", description="ISO 15924 script code (lowercase)")
    translation_lang: str | None = Field(None, description="ISO 639-3 code of the translation language")
    translation_script: str | None = Field(None, description="ISO 15924 script code of the translation language")
    level: str | None = Field(None, description="CEFR level a1..c2 (lowercase)")
    date: str | None = Field(None, description="ISO date YYYY-MM-DD")
    author: str | None = None
    vocabulary: list[VocabularyEntry] = Field(default_factory=list)
    models: list[ModelEntry] = Field(default_factory=list)
    source: Source | None = None
    transcription: str | None = None
    translation: str | None = None
    translation_dialog: DialogSource | None = None
    grammar: str | None = Field(
        None,
        description="Grammar block as Markdown prose (in the translation language).",
    )
    questions: list[str] | None = None
    exercises: list[Exercise] = Field(default_factory=list)
