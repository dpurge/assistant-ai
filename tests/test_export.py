"""End-to-end tests for the export tools (typst + anki).

Tests run the actual CLIs via subprocess and diff against committed golden
files in tests/golden/. Regenerate goldens with `just test-update-golden`
when an intentional output change lands.
"""

from __future__ import annotations

import pytest

from conftest import (
    ANKI_TOOL,
    FIXTURES,
    GOLDEN,
    MDX_TOOL,
    TYPST_TOOL,
    run_tool,
)


# --- golden output tests ----------------------------------------------------

@pytest.mark.parametrize("fixture", ["diana", "farsi-dialog"])
def test_typst_golden(fixture: str):
    fixture_path = FIXTURES / f"{fixture}.json"
    golden_path = GOLDEN / f"{fixture}.typ"
    result = run_tool(TYPST_TOOL, "--in", str(fixture_path))
    assert result.returncode == 0, f"stderr: {result.stderr}"
    assert result.stdout == golden_path.read_text(encoding="utf-8"), (
        f"typst-export drift on {fixture}.json — regenerate golden with:\n"
        f"  uv run --script {TYPST_TOOL} --in {fixture_path} --out {golden_path}"
    )


@pytest.mark.parametrize("fixture", ["diana", "farsi-dialog"])
def test_anki_golden(fixture: str):
    fixture_path = FIXTURES / f"{fixture}.json"
    golden_path = GOLDEN / f"{fixture}.tsv"
    result = run_tool(ANKI_TOOL, "--in", str(fixture_path))
    assert result.returncode == 0, f"stderr: {result.stderr}"
    assert result.stdout == golden_path.read_text(encoding="utf-8"), (
        f"anki-export drift on {fixture}.json — regenerate golden with:\n"
        f"  uv run --script {ANKI_TOOL} --in {fixture_path} --out {golden_path}"
    )


@pytest.mark.parametrize("fixture", ["diana", "farsi-dialog"])
def test_mdx_golden(fixture: str):
    fixture_path = FIXTURES / f"{fixture}.json"
    golden_path = GOLDEN / f"{fixture}.mdx"
    result = run_tool(MDX_TOOL, "--in", str(fixture_path))
    assert result.returncode == 0, f"stderr: {result.stderr}"
    assert result.stdout == golden_path.read_text(encoding="utf-8"), (
        f"mdx-export drift on {fixture}.json — regenerate golden with:\n"
        f"  uv run --script {MDX_TOOL} --in {fixture_path} --out {golden_path}"
    )


def test_mdx_grammar_section():
    """The optional `grammar` field renders as a `## Gramatyka` section."""
    fixture_path = FIXTURES / "diana-grammar.json"
    golden_path = GOLDEN / "diana-grammar.mdx"
    result = run_tool(MDX_TOOL, "--in", str(fixture_path))
    assert result.returncode == 0, f"stderr: {result.stderr}"
    assert "## Gramatyka" in result.stdout
    assert result.stdout == golden_path.read_text(encoding="utf-8"), (
        f"mdx-export grammar drift — regenerate golden with:\n"
        f"  uv run --script {MDX_TOOL} --in {fixture_path} --out {golden_path}"
    )


def test_mdx_no_grammar_section_when_absent():
    """No grammar field ⇒ no Gramatyka section (backward-compatible)."""
    result = run_tool(MDX_TOOL, stdin='{"title":"x","lang":"lat"}')
    assert result.returncode == 0
    assert "Gramatyka" not in result.stdout


# --- validation error tests -------------------------------------------------

@pytest.mark.parametrize("tool", [TYPST_TOOL, ANKI_TOOL, MDX_TOOL])
def test_missing_required_lang(tool):
    result = run_tool(tool, stdin='{"title": "x"}')
    assert result.returncode == 1
    assert "lang" in result.stderr
    assert "Field required" in result.stderr or "missing" in result.stderr.lower()


@pytest.mark.parametrize("tool", [TYPST_TOOL, ANKI_TOOL, MDX_TOOL])
def test_missing_required_title(tool):
    result = run_tool(tool, stdin='{"lang": "lat"}')
    assert result.returncode == 1
    assert "title" in result.stderr


def test_typst_bad_source_kind():
    result = run_tool(
        TYPST_TOOL,
        stdin='{"title":"x","lang":"lat","source":{"kind":"poem","content":"x"}}',
    )
    assert result.returncode == 1
    assert "source" in result.stderr
    # Pydantic discriminator error mentions valid tags
    assert "text" in result.stderr and "dialog" in result.stderr


@pytest.mark.parametrize("tool", [TYPST_TOOL, ANKI_TOOL, MDX_TOOL])
def test_malformed_json(tool):
    result = run_tool(tool, stdin='not json at all')
    assert result.returncode == 1
    assert "invalid JSON" in result.stderr or "JSON" in result.stderr


# --- schema introspection ---------------------------------------------------

@pytest.mark.parametrize("tool", [TYPST_TOOL, ANKI_TOOL, MDX_TOOL])
def test_print_schema(tool):
    result = run_tool(tool, "--print-schema")
    assert result.returncode == 0
    # JSON Schema includes $defs and properties keys
    assert '"$defs"' in result.stdout
    assert '"Lesson"' in result.stdout
    assert '"VocabularyEntry"' in result.stdout


def test_schemas_are_identical_across_tools():
    """All three export tools must agree on the lesson contract."""
    typst_schema = run_tool(TYPST_TOOL, "--print-schema").stdout
    anki_schema = run_tool(ANKI_TOOL, "--print-schema").stdout
    mdx_schema = run_tool(MDX_TOOL, "--print-schema").stdout
    assert typst_schema == anki_schema, "schema drift between phraseforge-typst and phraseforge-anki"
    assert typst_schema == mdx_schema, "schema drift between phraseforge-typst and phraseforge-web"


# --- models always carry translation ----------------------------------------

def test_typst_models_render_with_translation():
    """Every model entry must supply pattern + translation; transcription optional."""
    payload = (
        '{"title":"M","lang":"lat","date":"2026-06-22","models":['
        '{"pattern":"plain phrase","translation":"prosta fraza"},'
        '{"pattern":"with romanization","transcription":"x","translation":"z transkrypcją"}'
        ']}'
    )
    result = run_tool(TYPST_TOOL, stdin=payload)
    assert result.returncode == 0
    assert "- plain phrase = prosta fraza" in result.stdout
    assert "- with romanization [x] = z transkrypcją" in result.stdout


def test_typst_model_without_translation_fails():
    """A model entry missing `translation` must be rejected by validation."""
    payload = '{"title":"M","lang":"lat","models":[{"pattern":"x"}]}'
    result = run_tool(TYPST_TOOL, stdin=payload)
    assert result.returncode == 1
    assert "translation" in result.stderr
