"""The single most important test in this repo: analysis_only must never reach a
candidate model. This checks every real case file, not a synthetic example, so it
fails immediately if a future case accidentally puts sensitive content somewhere
build_candidate_prompt() picks up.
"""

from src.case_loader import build_candidate_prompt, load_all_cases


def test_analysis_only_never_in_prompt():
    for case in load_all_cases():
        prompt = build_candidate_prompt(case)
        analysis = case.get("analysis_only", {})
        for key, value in analysis.items():
            if not isinstance(value, str):
                continue
            snippet = value.strip()
            assert snippet, "empty analysis_only.{} in case {}".format(key, case["id"])
            assert snippet not in prompt, "analysis_only.{} leaked into prompt for case {}".format(
                key, case["id"]
            )


def test_analysis_only_key_not_in_prompt_text():
    for case in load_all_cases():
        prompt = build_candidate_prompt(case)
        assert "analysis_only" not in prompt
        assert "historical_decision" not in prompt
        assert "eventual_outcome" not in prompt
