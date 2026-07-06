# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "openai>=1.0",
#   "pyyaml>=6.0",
# ]
# ///
"""Skill evaluation harness for assistant-ai.

Sends each case from tests/eval/cases.yaml to an OpenAI-compat model and
scores responses on skill-loading conventions and golden similarity.
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from datetime import date
from pathlib import Path
from statistics import mean
from typing import Any

import openai
import yaml


# ---------------------------------------------------------------------------
# Case loading
# ---------------------------------------------------------------------------

def _substitute(template: str, variables: dict) -> str:
    """Replace {key} placeholders in template without touching other braces.

    Uses plain string replacement so JSON content (which is full of { and })
    is never mis-parsed as a format string.
    """
    result = template
    for key, val in variables.items():
        result = result.replace(f"{{{key}}}", str(val))
    return result


def load_cases(yaml_path: Path, skill_root: Path) -> list[dict]:
    """Load and expand template cases from the YAML manifest."""
    with open(yaml_path, encoding="utf-8") as fh:
        manifest = yaml.safe_load(fh)

    expanded: list[dict] = []
    for case in manifest["cases"]:
        if case.get("template"):
            template_golden = case.get("golden", "")
            for var in case.get("variables", []):
                # Separate substitution vars from the per-entry golden override.
                var_golden = var.pop("golden", None) if isinstance(var, dict) else None
                var_dict = {k: str(v) for k, v in var.items()}

                # Per-variable golden overrides template golden; both get substituted.
                raw_golden = var_golden if var_golden is not None else template_golden
                expanded.append({
                    "id": _substitute(case["id"], var_dict),
                    "skills": [_substitute(s, var_dict) for s in case["skills"]],
                    "prompt": _substitute(case["prompt"], var_dict),
                    "message": _substitute(case["message"], var_dict),
                    "golden": _substitute(raw_golden, var_dict),
                })
        else:
            expanded.append({
                "id": case["id"],
                "skills": case["skills"],
                "prompt": case["prompt"],
                "message": case["message"],
                "golden": case.get("golden", ""),
            })

    return expanded


# ---------------------------------------------------------------------------
# Skill text loading
# ---------------------------------------------------------------------------

def load_skill_text(skill_root: Path, name: str) -> str:
    """Read SKILL.md for the given skill name; raise FileNotFoundError if missing."""
    skill_file = skill_root / name / "SKILL.md"
    if not skill_file.exists():
        raise FileNotFoundError(f"SKILL.md not found: {skill_file}")
    return skill_file.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Message building
# ---------------------------------------------------------------------------

def build_messages(case: dict, skills_text: dict[str, str]) -> tuple[str, str]:
    """Build (system, user) pair from case + loaded skill texts."""
    skill_blocks = []
    for skill_name in case["skills"]:
        text = skills_text.get(skill_name, "")
        if text:
            skill_blocks.append(f"## Skill: {skill_name}\n\n{text}")

    system = case["prompt"].strip()
    if skill_blocks:
        system = system + "\n\n---\n\n" + "\n\n---\n\n".join(skill_blocks)

    return system, case["message"].strip()


# ---------------------------------------------------------------------------
# Model call
# ---------------------------------------------------------------------------

def call_model(
    system: str,
    user: str,
    base_url: str,
    model: str,
    api_key: str,
    timeout: int = 120,
) -> str:
    """Call an OpenAI-compat chat completion endpoint; return response text."""
    client = openai.OpenAI(
        base_url=base_url,
        api_key=api_key,
        timeout=timeout,
    )
    response = client.chat.completions.create(
        model=model,
        temperature=0,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )
    return response.choices[0].message.content or ""


# ---------------------------------------------------------------------------
# Skill loading scoring
# ---------------------------------------------------------------------------

def score_skill_loading(response: str, skill_names: list[str]) -> float:
    """Heuristic check that the model followed skill-specific conventions."""
    scores: list[float] = []

    for name in skill_names:
        if name == "phraseforge-core":
            has_vocab = "vocabulary" in response
            has_models = "models" in response
            if has_vocab and has_models:
                scores.append(1.0)
            elif has_vocab or has_models:
                scores.append(0.5)
            else:
                scores.append(0.0)

        elif name.startswith("phraseforge-lang-"):
            code = name[len("phraseforge-lang-"):]
            try:
                parsed = json.loads(_extract_json(response))
                scores.append(1.0 if parsed.get("lang") == code else 0.0)
            except (json.JSONDecodeError, ValueError):
                # Fallback: require "lang": "code" pattern, not bare code anywhere
                pattern = rf'"lang"\s*:\s*"{re.escape(code)}"'
                scores.append(1.0 if re.search(pattern, response) else 0.0)

        elif name == "research-core":
            has_summary = "## Summary" in response
            has_references = "## References" in response
            fraction = sum([has_summary, has_references]) / 2.0
            scores.append(fraction)

        elif name == "phraseforge-web":
            scores.append(1.0 if "import" in response else 0.0)

        elif name == "phraseforge-anki":
            scores.append(1.0 if "\t" in response else 0.0)

        elif name == "phraseforge-typst":
            has_hash_at_start = any(
                line.startswith("#") for line in response.splitlines()
            )
            scores.append(1.0 if has_hash_at_start else 0.0)

        elif name == "research-web":
            # research-web produces Docusaurus MDX — check for frontmatter or heading
            has_heading = any(
                line.startswith("#") for line in response.splitlines()
            )
            scores.append(1.0 if has_heading else 0.0)

    if not scores:
        return 0.5  # no applicable heuristic → neutral
    return mean(scores)


def _extract_json(text: str) -> str:
    """Best-effort: return the first fenced code block, or the raw text if no fence found."""
    text = text.strip()
    m = re.search(r"```(?:\w+)?\n(.*?)```", text, re.DOTALL)
    if m:
        return m.group(1).strip()
    return text


# ---------------------------------------------------------------------------
# Golden similarity scoring
# ---------------------------------------------------------------------------

def _json_field_coverage(golden_obj: Any, response_obj: Any) -> float:
    """Recursively compute fraction of golden fields present in response."""
    if not isinstance(golden_obj, dict):
        # Leaf comparison
        if isinstance(golden_obj, str) and isinstance(response_obj, str):
            ratio = difflib.SequenceMatcher(
                None, golden_obj, response_obj
            ).ratio()
            return 1.0 if ratio >= 0.4 else 0.0
        return 1.0 if golden_obj == response_obj else 0.0

    if not isinstance(response_obj, dict):
        return 0.0

    matched = 0
    for key, g_val in golden_obj.items():
        if key not in response_obj:
            continue
        r_val = response_obj[key]
        if isinstance(g_val, list):
            # Array: fraction of golden items matched by any response item
            if not isinstance(r_val, list) or not g_val:
                matched += 0
                continue
            item_scores = []
            for g_item in g_val:
                best = max(
                    (_json_field_coverage(g_item, r_item) for r_item in r_val),
                    default=0.0,
                )
                item_scores.append(best)
            matched += mean(item_scores)
        elif isinstance(g_val, dict):
            matched += _json_field_coverage(g_val, r_val)
        elif isinstance(g_val, str):
            ratio = difflib.SequenceMatcher(None, str(g_val), str(r_val)).ratio()
            matched += 1.0 if ratio >= 0.4 else 0.0
        else:
            matched += 1.0 if g_val == r_val else 0.0

    return matched / len(golden_obj) if golden_obj else 1.0


def score_golden_similarity(response: str, golden: str) -> float:
    """Score 0–1 similarity between response and golden answer."""
    response_clean = _extract_json(response)
    golden_clean = _extract_json(golden)

    try:
        r_obj = json.loads(response_clean)
        g_obj = json.loads(golden_clean)
        return _json_field_coverage(g_obj, r_obj)
    except (json.JSONDecodeError, ValueError):
        pass

    # Fall back to string similarity on the raw texts
    return difflib.SequenceMatcher(None, response, golden).ratio()


# ---------------------------------------------------------------------------
# Combined case scoring
# ---------------------------------------------------------------------------

def score_case(
    sl: float, gs: float
) -> int:
    """Return combined score 0–100 from pre-computed skill_loading and golden_similarity."""
    return round((0.40 * sl + 0.60 * gs) * 100)


# ---------------------------------------------------------------------------
# Report writing
# ---------------------------------------------------------------------------

def write_report(
    results: list[dict],
    model: str,
    base_url: str,
    output_path: Path,
) -> None:
    """Write Markdown evaluation report to output_path."""
    agg = round(mean(r["score"] for r in results)) if results else 0
    today = date.today().isoformat()

    lines: list[str] = [
        "# Skill Evaluation Report",
        "",
        f"**Model:** {model}  ",
        f"**Base URL:** {base_url}  ",
        f"**Date:** {today}  ",
        f"**Aggregate Score: {agg} / 100**",
        "",
        "---",
        "",
        "## Results",
        "",
        "| Skill | Score | Skill Loading | Golden Similarity | Status |",
        "|-------|-------|---------------|-------------------|--------|",
    ]

    for r in results:
        score = r["score"]
        if score >= 70:
            status = "✅"
        elif score >= 50:
            status = "⚠️"
        else:
            status = "❌"
        sl = f"{r['skill_loading']:.2f}"
        gs = f"{r['golden_similarity']:.2f}"
        lines.append(
            f"| {r['id']} | {score} | {sl} | {gs} | {status} |"
        )

    failed = [r for r in results if r["score"] < 70]
    if failed:
        lines += ["", "---", "", "## Failed / Degraded Cases", ""]
        for r in failed:
            score = r["score"]
            lines.append(f"### {r['id']} ({score}/100)")
            if r.get("error"):
                lines.append(f"**Error:** {r['error']}")
            else:
                if r["skill_loading"] < 0.7:
                    lines.append(
                        f"**Skill loading issues:** score={r['skill_loading']:.2f}"
                    )
                if r["golden_similarity"] < 0.7:
                    lines.append(
                        f"**Golden delta:** similarity={r['golden_similarity']:.2f}"
                    )
                snippet = r.get("response", "")[:500].replace("\n", "\n> ")
                lines.append("**Response (first 500 chars):**")
                lines.append(f"> {snippet}")
            lines.append("")

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Evaluate skill prompt quality against an OpenAI-compat model."
    )
    parser.add_argument("--model", default="gemma2:2b", help="Model name")
    parser.add_argument(
        "--base-url",
        default="http://localhost:11434/v1",
        help="OpenAI-compat API base URL",
    )
    parser.add_argument(
        "--api-key",
        default="ollama",
        help="API key (use any non-empty value for local Ollama)",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output report path (default: tests/eval/report.md)",
    )
    parser.add_argument(
        "--skill",
        default=None,
        help="Evaluate a single skill by id (substring match)",
    )
    args = parser.parse_args()

    project_root = Path(__file__).parent.parent
    yaml_path = project_root / "tests" / "eval" / "cases.yaml"
    skill_root = project_root / "content" / "skills"
    output_path = Path(args.output) if args.output else project_root / "tests" / "eval" / "report.md"

    cases = load_cases(yaml_path, skill_root)

    if args.skill:
        cases = [c for c in cases if args.skill in c["id"]]
        if not cases:
            print(f"No cases match --skill={args.skill!r}", file=sys.stderr)
            sys.exit(0)

    results: list[dict] = []

    for case in cases:
        case_id = case["id"]
        print(f"Evaluating {case_id}...", file=sys.stderr)

        # Load skill texts
        skills_text: dict[str, str] = {}
        missing_skills: list[str] = []
        for skill_name in case["skills"]:
            try:
                skills_text[skill_name] = load_skill_text(skill_root, skill_name)
            except FileNotFoundError:
                missing_skills.append(skill_name)

        if missing_skills:
            results.append({
                "id": case_id,
                "score": 0,
                "skill_loading": 0.0,
                "golden_similarity": 0.0,
                "response": "",
                "error": f"Missing SKILL.md for: {', '.join(missing_skills)}",
            })
            continue

        system, user = build_messages(case, skills_text)

        try:
            response = call_model(
                system=system,
                user=user,
                base_url=args.base_url,
                model=args.model,
                api_key=args.api_key,
            )
            error = None
        except Exception as exc:  # noqa: BLE001
            response = ""
            error = str(exc)

        if error:
            results.append({
                "id": case_id,
                "score": 0,
                "skill_loading": 0.0,
                "golden_similarity": 0.0,
                "response": response,
                "error": error,
            })
            continue

        sl = score_skill_loading(response, case["skills"])
        gs = score_golden_similarity(response, case["golden"])
        score = score_case(sl, gs)

        results.append({
            "id": case_id,
            "score": score,
            "skill_loading": sl,
            "golden_similarity": gs,
            "response": response,
            "error": None,
        })

    write_report(results, model=args.model, base_url=args.base_url, output_path=output_path)

    agg = round(mean(r["score"] for r in results)) if results else 0
    print(f"Report written to: {output_path}", file=sys.stderr)
    print(f"AGGREGATE: {agg}")

    sys.exit(0)


if __name__ == "__main__":
    main()
