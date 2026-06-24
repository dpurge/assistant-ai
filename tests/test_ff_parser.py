"""Tests for the ff-parser.py PhraseForge source file parser.

All CLI tests run via `uv run --script` (same approach as test_export.py).
Fixture files are fragments of real data from phraseforge-data/dat/.
Dialog parsing is exercised inline via stdin since no dialog *.ff files
exist in the real data.
"""

from __future__ import annotations

import json
from pathlib import Path

from conftest import FIXTURES, run_tool

FF_PARSER = (
    Path(__file__).resolve().parent.parent
    / "content"
    / "skills"
    / "phraseforge-core"
    / "tools"
    / "ff-parser.py"
)

# Real data fragments used as fixtures
ARB_FF = FIXTURES / "bagauddin-1992-arb.ff"   # arb-arab → pol-latn, no transcription
DEU_FF = FIXTURES / "frequency-deu.ff"         # deu-latn → eng-latn, notes + multi-translation


# ---------------------------------------------------------------------------
# Arabic vocabulary (bagauddin-1992-arb.ff)
# Non-Latin script, grammar tags {sg}/{pl}, two chunks
# ---------------------------------------------------------------------------

class TestArabicVocabulary:

    def test_header_fields(self):
        result = run_tool(FF_PARSER, str(ARB_FF), "--chunk", "1")
        assert result.returncode == 0, f"stderr: {result.stderr}"
        data = json.loads(result.stdout)
        assert data["lang"] == "arb"
        assert data["script"] == "arab"
        assert data["translation_lang"] == "pol"
        assert data["translation_script"] == "latn"
        assert data["description"] == "Bagauddin 1992"

    def test_headwords_present(self):
        result = run_tool(FF_PARSER, str(ARB_FF), "--chunk", "1")
        data = json.loads(result.stdout)
        headwords = {e["headword"] for e in data["vocabulary"]}
        assert "هُوَ" in headwords
        assert "كَبِيرٌ" in headwords

    def test_grammar_tag_sg(self):
        result = run_tool(FF_PARSER, str(ARB_FF), "--chunk", "1")
        data = json.loads(result.stdout)
        kabir = next(e for e in data["vocabulary"] if e["headword"] == "كَبِيرٌ")
        assert kabir["grammar"] == "sg"
        assert kabir["translation"] == "duży"

    def test_grammar_tag_pl(self):
        result = run_tool(FF_PARSER, str(ARB_FF), "--chunk", "1")
        data = json.loads(result.stdout)
        kibar = next(e for e in data["vocabulary"] if e["headword"] == "كِبَارٌ")
        assert kibar["grammar"] == "pl"

    def test_no_transcription_in_real_data(self):
        result = run_tool(FF_PARSER, str(ARB_FF), "--chunk", "1")
        data = json.loads(result.stdout)
        # Real bagauddin data has no romanization — transcription should be absent
        for entry in data["vocabulary"]:
            assert entry.get("transcription") is None

    def test_second_chunk_has_feminine_forms(self):
        result = run_tool(FF_PARSER, str(ARB_FF), "--chunk", "2")
        assert result.returncode == 0
        data = json.loads(result.stdout)
        headwords = {e["headword"] for e in data["vocabulary"]}
        assert "هِىَ" in headwords       # she
        assert "كَبِيرَةٌ" in headwords  # big (f. sg.)

    def test_all_chunks_returns_two_element_array(self):
        result = run_tool(FF_PARSER, str(ARB_FF))
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert isinstance(data, list)
        assert len(data) == 2


# ---------------------------------------------------------------------------
# German vocabulary (frequency-deu.ff)
# Latin script, notes in parentheses, semicolon-separated translations
# ---------------------------------------------------------------------------

class TestGermanVocabulary:

    def test_header_fields(self):
        result = run_tool(FF_PARSER, str(DEU_FF), "--chunk", "1")
        assert result.returncode == 0, f"stderr: {result.stderr}"
        data = json.loads(result.stdout)
        assert data["lang"] == "deu"
        assert data["script"] == "latn"
        assert data["translation_lang"] == "eng"
        assert data["translation_script"] == "latn"
        assert data["description"] == "Frequency vocabulary"

    def test_simple_entry(self):
        result = run_tool(FF_PARSER, str(DEU_FF), "--chunk", "1")
        data = json.loads(result.stdout)
        sein = next(e for e in data["vocabulary"] if e["headword"] == "sein")
        assert sein["grammar"] == "verb"
        assert sein["translation"] == "to be"
        assert sein.get("notes") is None

    def test_note_extracted_from_parenthetical(self):
        result = run_tool(FF_PARSER, str(DEU_FF), "--chunk", "1")
        data = json.loads(result.stdout)
        sie = next(e for e in data["vocabulary"] if e["headword"] == "Sie")
        assert sie["translation"] == "you"
        assert sie["notes"] == "formal"

    def test_multiple_translations_joined(self):
        result = run_tool(FF_PARSER, str(DEU_FF), "--chunk", "1")
        data = json.loads(result.stdout)
        auch = next(e for e in data["vocabulary"] if e["headword"] == "auch")
        assert auch["translation"] == "also; too"

    def test_second_chunk_headwords(self):
        result = run_tool(FF_PARSER, str(DEU_FF), "--chunk", "2")
        assert result.returncode == 0
        data = json.loads(result.stdout)
        headwords = {e["headword"] for e in data["vocabulary"]}
        assert "mehr" in headwords
        assert "immer" in headwords

    def test_chunk_title_contains_document_and_id(self):
        result = run_tool(FF_PARSER, str(DEU_FF), "--chunk", "1")
        data = json.loads(result.stdout)
        assert "frequency" in data["title"]
        assert "1" in data["title"]


# ---------------------------------------------------------------------------
# Dialog parsing — exercised with inline stdin content
# (No dialog *.ff files exist in the real data corpus.)
# ---------------------------------------------------------------------------

_DIALOG_FF = """\
document: dialog-test
type: dialog
description: Named speaker dialog
data:
  language: lat
  script: latn
translation:
  language: pol
  script: latn

=== 1 ===

# De schola

@Marcus:
  Salve, Quinte!

@Quintus:
  Salve, Marce!

  Quid agis?

@Marcus:
  Bene valeo, gratias.
"""

_DIALOG_FF_ANON = """\
document: dialog-anon-test
type: dialog
description: Anonymous turn dialog
data:
  language: lat
  script: latn
translation:
  language: pol
  script: latn

=== 1 ===

Scaena in foro Romano.

--:
  Civis adpropinquat.

--:
  Alius civis respondet.
"""


class TestDialogParsing:

    def test_named_speakers_dialog(self):
        result = run_tool(FF_PARSER, "-", "--chunk", "1", stdin=_DIALOG_FF)
        assert result.returncode == 0, f"stderr: {result.stderr}"
        data = json.loads(result.stdout)
        assert data["source"]["kind"] == "dialog"

    def test_dialog_title_extracted(self):
        result = run_tool(FF_PARSER, "-", "--chunk", "1", stdin=_DIALOG_FF)
        data = json.loads(result.stdout)
        assert data["source"]["title"] == "De schola"

    def test_named_speaker_turns(self):
        result = run_tool(FF_PARSER, "-", "--chunk", "1", stdin=_DIALOG_FF)
        data = json.loads(result.stdout)
        speakers = {i.get("speaker") for i in data["source"]["items"]
                    if i["kind"] == "turn"}
        assert "Marcus" in speakers
        assert "Quintus" in speakers

    def test_multi_paragraph_turn(self):
        result = run_tool(FF_PARSER, "-", "--chunk", "1", stdin=_DIALOG_FF)
        data = json.loads(result.stdout)
        quintus = next(i for i in data["source"]["items"]
                       if i.get("speaker") == "Quintus")
        assert len(quintus["paragraphs"]) == 2

    def test_anonymous_turns_only(self):
        result = run_tool(FF_PARSER, "-", "--chunk", "1", stdin=_DIALOG_FF_ANON)
        assert result.returncode == 0, f"stderr: {result.stderr}"
        data = json.loads(result.stdout)
        turns = [i for i in data["source"]["items"] if i["kind"] == "turn"]
        assert len(turns) == 2
        assert all(t.get("speaker") is None for t in turns)

    def test_narration_before_anonymous_turns(self):
        result = run_tool(FF_PARSER, "-", "--chunk", "1", stdin=_DIALOG_FF_ANON)
        data = json.loads(result.stdout)
        narrations = [i for i in data["source"]["items"] if i["kind"] == "narration"]
        assert len(narrations) == 1
        assert "foro" in narrations[0]["text"]


# ---------------------------------------------------------------------------
# Schema introspection
# ---------------------------------------------------------------------------

class TestSchema:

    def test_print_schema_exits_0(self):
        result = run_tool(FF_PARSER, "--print-schema")
        assert result.returncode == 0

    def test_schema_contains_translation_lang(self):
        result = run_tool(FF_PARSER, "--print-schema")
        schema = json.loads(result.stdout)
        assert "translation_lang" in schema.get("properties", {})

    def test_schema_matches_export_tools(self):
        """ff-parser must agree on the Lesson schema with the export tools."""
        from conftest import TYPST_TOOL
        ff_schema = run_tool(FF_PARSER, "--print-schema").stdout
        typst_schema = run_tool(TYPST_TOOL, "--print-schema").stdout
        assert ff_schema == typst_schema, "schema drift between ff-parser and phraseforge-typst"


# ---------------------------------------------------------------------------
# Error handling
# ---------------------------------------------------------------------------

class TestErrors:

    def test_missing_file_exits_1(self):
        result = run_tool(FF_PARSER, "does-not-exist.ff")
        assert result.returncode == 1
        assert "not found" in result.stderr

    def test_no_input_arg_exits_1(self):
        result = run_tool(FF_PARSER)
        assert result.returncode == 1

    def test_out_of_range_chunk_exits_0_with_warning(self):
        result = run_tool(FF_PARSER, str(ARB_FF), "--chunk", "999")
        assert result.returncode == 0
        assert "warning" in result.stderr.lower()
