"""Unit tests for scripts/eval_skills.py — mocks the model client."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Load the eval_skills module without going through uv PEP-723 runner.
SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

spec = importlib.util.spec_from_file_location(
    "eval_skills", SCRIPTS_DIR / "eval_skills.py"
)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


# ---------------------------------------------------------------------------
# _extract_json
# ---------------------------------------------------------------------------

class TestSubstitute:
    def test_replaces_known_placeholders(self):
        assert m._substitute("lang is {code}", {"code": "deu"}) == "lang is deu"

    def test_leaves_json_braces_untouched(self):
        golden = '{"lang": "{code}", "vocabulary": []}'
        result = m._substitute(golden, {"code": "deu"})
        assert result == '{"lang": "deu", "vocabulary": []}'

    def test_unknown_placeholder_left_as_is(self):
        assert m._substitute("hello {unknown}", {"code": "deu"}) == "hello {unknown}"

    def test_multiple_occurrences(self):
        assert m._substitute("{a} and {a}", {"a": "x"}) == "x and x"


class TestExtractJson:
    def test_plain_json(self):
        text = '{"lang": "deu"}'
        assert m._extract_json(text) == text

    def test_fenced_json_no_prefix(self):
        text = '```json\n{"lang": "deu"}\n```'
        assert json.loads(m._extract_json(text))["lang"] == "deu"

    def test_fenced_json_with_prose_before(self):
        text = 'Here is the result:\n```json\n{"lang": "deu"}\n```'
        assert json.loads(m._extract_json(text))["lang"] == "deu"

    def test_no_fence_returns_stripped(self):
        text = "  hello world  "
        assert m._extract_json(text) == "hello world"


# ---------------------------------------------------------------------------
# score_skill_loading
# ---------------------------------------------------------------------------

GOOD_DEU_JSON = json.dumps({
    "lang": "deu",
    "vocabulary": [{"headword": "Hallo", "grammar": "Interj", "translation": "cześć"}],
    "models": [{"pattern": "Wie geht es?", "translation": "Jak się masz?"}],
})


class TestScoreSkillLoading:
    def test_phraseforge_core_full_score(self):
        sl = m.score_skill_loading(GOOD_DEU_JSON, ["phraseforge-core"])
        assert sl == 1.0

    def test_phraseforge_core_partial(self):
        text = '{"vocabulary": []}'
        sl = m.score_skill_loading(text, ["phraseforge-core"])
        assert sl == 0.5

    def test_phraseforge_core_zero(self):
        sl = m.score_skill_loading("I cannot help.", ["phraseforge-core"])
        assert sl == 0.0

    def test_phraseforge_lang_correct_lang_field(self):
        sl = m.score_skill_loading(GOOD_DEU_JSON, ["phraseforge-lang-deu"])
        assert sl == 1.0

    def test_phraseforge_lang_wrong_lang_field(self):
        wrong = json.dumps({"lang": "fra"})
        sl = m.score_skill_loading(wrong, ["phraseforge-lang-deu"])
        assert sl == 0.0

    def test_phraseforge_lang_fallback_requires_key_value_pattern(self):
        # Bare code present in prose but not as "lang": "deu" — should score 0
        prose = 'Sorry, I cannot process deu language content.'
        sl = m.score_skill_loading(prose, ["phraseforge-lang-deu"])
        assert sl == 0.0

    def test_phraseforge_lang_fallback_accepts_key_value_pattern(self):
        # No JSON but the JSON pattern is embedded in prose
        text = 'Result: "lang": "deu", more text.'
        sl = m.score_skill_loading(text, ["phraseforge-lang-deu"])
        assert sl == 1.0

    def test_research_core_both_sections(self):
        text = "## Summary\n\nSome text.\n\n## References\n\n- [wiki:x]"
        sl = m.score_skill_loading(text, ["research-core"])
        assert sl == 1.0

    def test_research_core_one_section(self):
        text = "## Summary\n\nSome text."
        sl = m.score_skill_loading(text, ["research-core"])
        assert sl == 0.5

    def test_research_core_no_sections(self):
        sl = m.score_skill_loading("Nothing here.", ["research-core"])
        assert sl == 0.0

    def test_phraseforge_web(self):
        assert m.score_skill_loading("import Foo from 'bar'", ["phraseforge-web"]) == 1.0
        assert m.score_skill_loading("No such keyword here.", ["phraseforge-web"]) == 0.0

    def test_phraseforge_anki_tab(self):
        assert m.score_skill_loading("word\ttranslation", ["phraseforge-anki"]) == 1.0
        assert m.score_skill_loading("word translation", ["phraseforge-anki"]) == 0.0

    def test_phraseforge_typst_hash_at_line_start(self):
        assert m.score_skill_loading("# Title\nText", ["phraseforge-typst"]) == 1.0
        assert m.score_skill_loading("no heading here", ["phraseforge-typst"]) == 0.0

    def test_mean_of_multiple_skills(self):
        # phraseforge-core: 1.0 (both vocab+models present), phraseforge-lang-deu: 1.0
        sl = m.score_skill_loading(GOOD_DEU_JSON, ["phraseforge-core", "phraseforge-lang-deu"])
        assert sl == 1.0

    def test_no_applicable_heuristic_returns_neutral(self):
        sl = m.score_skill_loading("anything", ["unknown-skill"])
        assert sl == 0.5


# ---------------------------------------------------------------------------
# score_golden_similarity
# ---------------------------------------------------------------------------

GOLDEN_DEU = json.dumps({
    "title": "Basic Greetings",
    "lang": "deu",
    "vocabulary": [{"headword": "Hallo", "grammar": "Interj", "translation": "cześć"}],
    "models": [{"pattern": "Wie geht es Ihnen?", "translation": "Jak się masz?"}],
})


class TestScoreGoldenSimilarity:
    def test_identical_json_scores_one(self):
        gs = m.score_golden_similarity(GOLDEN_DEU, GOLDEN_DEU)
        assert gs == 1.0

    def test_similar_json_scores_high(self):
        # Same structure, slightly different values
        response = json.dumps({
            "title": "Greetings",
            "lang": "deu",
            "vocabulary": [{"headword": "Hallo", "grammar": "Interj", "translation": "hej"}],
            "models": [{"pattern": "Wie geht es?", "translation": "Jak sie masz?"}],
        })
        gs = m.score_golden_similarity(response, GOLDEN_DEU)
        assert gs >= 0.7

    def test_empty_response_scores_low(self):
        gs = m.score_golden_similarity("", GOLDEN_DEU)
        assert gs < 0.2

    def test_empty_golden_scores_zero(self):
        gs = m.score_golden_similarity(GOOD_DEU_JSON, "")
        assert gs == 0.0

    def test_fenced_json_response(self):
        fenced = f"Here is the result:\n```json\n{GOLDEN_DEU}\n```"
        gs = m.score_golden_similarity(fenced, GOLDEN_DEU)
        assert gs == 1.0

    def test_markdown_fallback_similar_text(self):
        golden = "## Summary\n\nRome fell.\n\n## References\n\n- [wiki:x]"
        response = "## Summary\n\nRome fell in 476 AD.\n\n## References\n\n- [wiki:x]"
        gs = m.score_golden_similarity(response, golden)
        assert gs >= 0.5

    def test_completely_wrong_response(self):
        gs = m.score_golden_similarity("The quick brown fox.", GOLDEN_DEU)
        assert gs < 0.2


# ---------------------------------------------------------------------------
# score_case
# ---------------------------------------------------------------------------

class TestScoreCase:
    def test_perfect_score(self):
        assert m.score_case(1.0, 1.0) == 100

    def test_zero_score(self):
        assert m.score_case(0.0, 0.0) == 0

    def test_weights(self):
        # 0.40 * 1.0 + 0.60 * 0.0 = 0.40 → 40
        assert m.score_case(1.0, 0.0) == 40
        # 0.40 * 0.0 + 0.60 * 1.0 = 0.60 → 60
        assert m.score_case(0.0, 1.0) == 60

    def test_typical_good_response(self):
        score = m.score_case(0.9, 0.85)
        assert 80 <= score <= 90


# ---------------------------------------------------------------------------
# load_cases — template expansion
# ---------------------------------------------------------------------------

class TestLoadCases:
    def test_expands_language_template(self, tmp_path):
        yaml_content = """
skill_root: content/skills
cases:
  - id: "phraseforge-lang-{code}"
    template: true
    skills:
      - phraseforge-core
      - "phraseforge-lang-{code}"
    prompt: "Extract vocab for {language_name}."
    message: "Greetings in {language_name}."
    golden: "template fallback"
    variables:
      - code: deu
        language_name: German
        golden: '{"lang":"deu"}'
      - code: fra
        language_name: French
"""
        yaml_path = tmp_path / "cases.yaml"
        yaml_path.write_text(yaml_content)
        cases = m.load_cases(yaml_path, tmp_path)
        assert len(cases) == 2
        deu = next(c for c in cases if c["id"] == "phraseforge-lang-deu")
        assert deu["skills"] == ["phraseforge-core", "phraseforge-lang-deu"]
        assert "German" in deu["prompt"]
        # Per-variable golden is used (no substitution needed here since it's plain JSON)
        assert deu["golden"] == '{"lang":"deu"}'

    def test_substitution_applied_to_all_fields(self, tmp_path):
        yaml_content = """
skill_root: content/skills
cases:
  - id: "skill-{code}"
    template: true
    skills: ["skill-{code}"]
    prompt: "Prompt for {lang_name}."
    message: "Message about {lang_name}."
    golden: '{"lang": "{code}", "title": "{lang_name}"}'
    variables:
      - code: lat
        lang_name: Latin
"""
        yaml_path = tmp_path / "cases.yaml"
        yaml_path.write_text(yaml_content)
        cases = m.load_cases(yaml_path, tmp_path)
        c = cases[0]
        assert c["id"] == "skill-lat"
        assert c["skills"] == ["skill-lat"]
        assert c["prompt"] == "Prompt for Latin."
        assert c["message"] == "Message about Latin."
        # JSON braces around "lang" are untouched; {code} and {lang_name} substituted
        assert c["golden"] == '{"lang": "lat", "title": "Latin"}'

    def test_uses_template_golden_as_fallback(self, tmp_path):
        yaml_content = """
skill_root: content/skills
cases:
  - id: "phraseforge-lang-{code}"
    template: true
    skills: ["phraseforge-lang-{code}"]
    prompt: "p"
    message: "m"
    golden: "fallback for {code}"
    variables:
      - code: zxx
        language_name: No language
"""
        yaml_path = tmp_path / "cases.yaml"
        yaml_path.write_text(yaml_content)
        cases = m.load_cases(yaml_path, tmp_path)
        assert cases[0]["golden"] == "fallback for zxx"

    def test_non_template_case_passes_through(self, tmp_path):
        yaml_content = """
skill_root: content/skills
cases:
  - id: research-core
    skills: [research-core]
    prompt: "Write a report."
    message: "Topic: Rome"
    golden: "## Summary"
"""
        yaml_path = tmp_path / "cases.yaml"
        yaml_path.write_text(yaml_content)
        cases = m.load_cases(yaml_path, tmp_path)
        assert len(cases) == 1
        assert cases[0]["id"] == "research-core"
        assert cases[0]["golden"] == "## Summary"


# ---------------------------------------------------------------------------
# Integration: main() with mocked model
# ---------------------------------------------------------------------------

class TestMainMocked:
    def test_main_creates_report(self, tmp_path, monkeypatch):
        """main() runs end-to-end with a mocked model client and creates a report."""
        # Minimal cases.yaml with one easy-to-score case
        yaml_content = """
skill_root: content/skills
cases:
  - id: phraseforge-core
    skills: [phraseforge-core]
    prompt: "Output JSON with vocabulary and models."
    message: "Create a lesson."
    golden: '{"title":"x","lang":"lat","vocabulary":[],"models":[]}'
"""
        cases_path = tmp_path / "cases.yaml"
        cases_path.write_text(yaml_content)

        # Fake skill directory
        skill_dir = tmp_path / "content" / "skills" / "phraseforge-core"
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text("# PhraseForge Core\nTest skill.\n")

        output_path = tmp_path / "report.md"

        # Mock the model response
        fake_response = json.dumps({
            "title": "Test",
            "lang": "lat",
            "vocabulary": [{"headword": "amor", "grammar": "N m", "translation": "miłość"}],
            "models": [{"pattern": "Te amo.", "translation": "Kocham cię."}],
        })

        original_load_cases = m.load_cases

        with patch("openai.OpenAI") as mock_openai:
            mock_client = MagicMock()
            mock_openai.return_value = mock_client
            mock_choice = MagicMock()
            mock_choice.message.content = fake_response
            mock_client.chat.completions.create.return_value = MagicMock(
                choices=[mock_choice]
            )

            monkeypatch.setattr(
                m, "load_cases",
                lambda _yaml, _root: original_load_cases(
                    cases_path, tmp_path / "content" / "skills"
                ),
            )

            test_args = [
                "--model", "test-model",
                "--base-url", "http://localhost:11434/v1",
                "--output", str(output_path),
            ]
            with patch("sys.argv", ["eval_skills.py"] + test_args):
                with pytest.raises(SystemExit) as exc_info:
                    m.main()
                assert exc_info.value.code == 0

        assert output_path.exists()
        report = output_path.read_text()
        assert "phraseforge-core" in report
        assert "Aggregate Score" in report
