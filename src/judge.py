"""Judge: scores a raw candidate response against its case's rubric.

Receives the rubric and the response, built via the same build_candidate_prompt()
used for the candidate call, so it sees exactly what the candidate saw, plus the
rubric. Never receives analysis_only and never receives which model or provider
produced the response. See SPEC.md Section 13 and docs/methodology.md.
"""

import json
import re

from src.case_loader import build_candidate_prompt

JUDGE_PROMPT_VERSION = "v1"

VERDICT_SCORES = {"met": 1.0, "partially_met": 0.5, "not_met": 0.0}
VALID_VERDICTS = set(VERDICT_SCORES.keys())


def build_judge_prompt(case, response_text, template):
    rubric_lines = []
    for c in case["rubric"]["criteria"]:
        rubric_lines.append("- id: {}\n  description: {}\n  weight: {}".format(
            c["id"], c["description"].strip(), c["weight"]
        ))
    rubric_block = "\n".join(rubric_lines)

    case_context = build_candidate_prompt(case)

    return "{}\n\n---\n\nSCENARIO AND QUESTION:\n\n{}\n\n---\n\nRUBRIC:\n\n{}\n\n---\n\nCANDIDATE RESPONSE:\n\n{}\n".format(
        template.strip(), case_context, rubric_block, response_text.strip()
    )


def parse_judge_output(text):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("No JSON object found in judge output: {!r}".format(text[:200]))
    parsed = json.loads(match.group(0))
    for entry in parsed.get("criteria", []):
        if entry.get("verdict") not in VALID_VERDICTS:
            raise ValueError("Invalid verdict {!r} for criterion {!r}".format(
                entry.get("verdict"), entry.get("id")
            ))
    return parsed


def score_criteria(case, judge_output):
    criteria_by_id = {c["id"]: c for c in case["rubric"]["criteria"]}
    scored = []
    weighted_sum = 0.0
    max_possible = 0.0

    for entry in judge_output["criteria"]:
        criterion = criteria_by_id.get(entry["id"])
        if criterion is None:
            continue
        verdict = entry["verdict"]
        score = VERDICT_SCORES[verdict]
        weight = criterion["weight"]
        weighted_sum += score * weight
        max_possible += weight
        scored.append({
            "id": entry["id"],
            "verdict": verdict,
            "score": score,
            "weight": weight,
            "justification": entry.get("justification", ""),
        })

    return scored, weighted_sum, max_possible
