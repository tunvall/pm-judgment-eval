import pytest

from src.alignment import build_alignment_prompt, parse_alignment_output
from src.case_loader import load_all_cases

DUMMY_TEMPLATE = "ALIGNMENT INSTRUCTIONS PLACEHOLDER"


def test_alignment_prompt_includes_historical_decision_on_purpose():
    """The one place historical_decision SHOULD appear in a judge prompt."""
    case = load_all_cases()[0]
    prompt = build_alignment_prompt(case, "some candidate response", DUMMY_TEMPLATE)
    assert case["analysis_only"]["historical_decision"].strip() in prompt


def test_alignment_prompt_includes_response_and_context():
    case = load_all_cases()[0]
    prompt = build_alignment_prompt(case, "UNIQUE_RESPONSE_MARKER", DUMMY_TEMPLATE)
    assert "UNIQUE_RESPONSE_MARKER" in prompt
    assert case["scenario"].strip() in prompt


def test_parse_alignment_output_valid():
    text = '{"alignment": "partially_aligned", "justification": "close but not exact"}'
    parsed = parse_alignment_output(text)
    assert parsed["alignment"] == "partially_aligned"


def test_parse_alignment_output_rejects_invalid_value():
    text = '{"alignment": "sort_of", "justification": "x"}'
    with pytest.raises(ValueError):
        parse_alignment_output(text)
