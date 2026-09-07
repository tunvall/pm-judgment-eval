from src.case_loader import load_all_cases
from src.judge import build_judge_prompt, parse_judge_output, score_criteria

DUMMY_TEMPLATE = "JUDGE INSTRUCTIONS PLACEHOLDER"


def test_judge_prompt_never_contains_analysis_only():
    for case in load_all_cases():
        prompt = build_judge_prompt(case, "some candidate response text", DUMMY_TEMPLATE)
        for key, value in case["analysis_only"].items():
            if not isinstance(value, str):
                continue
            snippet = value.strip()
            assert snippet not in prompt, "analysis_only.{} leaked into judge prompt for {}".format(
                key, case["id"]
            )


def test_judge_prompt_includes_rubric_and_response():
    case = load_all_cases()[0]
    prompt = build_judge_prompt(case, "UNIQUE_RESPONSE_MARKER", DUMMY_TEMPLATE)
    assert "UNIQUE_RESPONSE_MARKER" in prompt
    for criterion in case["rubric"]["criteria"]:
        assert criterion["id"] in prompt


def test_parse_judge_output_extracts_json_from_markdown_fence():
    text = "Here you go:\n```json\n{\"criteria\": [{\"id\": \"x\", \"verdict\": \"met\", \"justification\": \"ok\"}]}\n```"
    parsed = parse_judge_output(text)
    assert parsed["criteria"][0]["id"] == "x"


def test_parse_judge_output_rejects_invalid_verdict():
    import pytest

    text = '{"criteria": [{"id": "x", "verdict": "sort_of", "justification": "ok"}]}'
    with pytest.raises(ValueError):
        parse_judge_output(text)


def test_score_criteria_weighted_sum():
    case = {
        "rubric": {
            "criteria": [
                {"id": "a", "description": "d", "weight": 3},
                {"id": "b", "description": "d", "weight": 2},
            ]
        }
    }
    judge_output = {
        "criteria": [
            {"id": "a", "verdict": "met", "justification": "j"},
            {"id": "b", "verdict": "not_met", "justification": "j"},
        ]
    }
    scored, weighted_sum, max_possible = score_criteria(case, judge_output)
    assert weighted_sum == 3.0
    assert max_possible == 5.0
    assert len(scored) == 2
