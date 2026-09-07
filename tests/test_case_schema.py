"""Schema validation for case files, per SPEC.md Section 9."""

from src.case_loader import load_all_cases

REQUIRED_TOP_LEVEL_FIELDS = (
    "id",
    "version",
    "title",
    "source",
    "dimensions",
    "difficulty",
    "scenario",
    "question",
    "rubric",
    "analysis_only",
)

REQUIRED_ANALYSIS_ONLY_FIELDS = ("historical_decision", "eventual_outcome", "case_author_notes")


def test_required_top_level_fields_present():
    for case in load_all_cases():
        for field in REQUIRED_TOP_LEVEL_FIELDS:
            assert field in case, "case {} missing required field: {}".format(case.get("id"), field)


def test_analysis_only_fields_present():
    for case in load_all_cases():
        for field in REQUIRED_ANALYSIS_ONLY_FIELDS:
            assert field in case["analysis_only"], "case {} missing analysis_only.{}".format(
                case["id"], field
            )


def test_rubric_criteria_well_formed():
    for case in load_all_cases():
        criteria = case["rubric"]["criteria"]
        assert len(criteria) > 0, "case {} has no rubric criteria".format(case["id"])
        for criterion in criteria:
            assert "id" in criterion
            assert "description" in criterion
            assert "weight" in criterion
            assert isinstance(criterion["weight"], (int, float))


def test_case_ids_are_unique():
    cases = load_all_cases()
    ids = [case["id"] for case in cases]
    assert len(ids) == len(set(ids)), "duplicate case ids found"


def test_case_ids_match_dimensions_from_spec():
    valid_dimensions = {
        "ambiguity",
        "evidence",
        "restraint",
        "tradeoff",
        "conviction",
        "calibration",
        "execution",
    }
    for case in load_all_cases():
        for dimension in case["dimensions"]:
            assert dimension in valid_dimensions, "case {} has unrecognized dimension: {}".format(
                case["id"], dimension
            )
