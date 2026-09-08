"""Decision-alignment scoring: a separate judge call comparing a candidate's stated
decision to the historical decision. Deliberately kept apart from src/judge.py:
this is the one judge call that is SUPPOSED to see analysis_only.historical_decision,
which the reasoning-quality judge must never see. Never blend alignment results
into the reasoning-quality weighted score; they answer different questions, per
docs/methodology.md.
"""

import json
import re

from src.case_loader import build_candidate_prompt

ALIGNMENT_PROMPT_VERSION = "v1"
VALID_ALIGNMENTS = {"aligned", "partially_aligned", "diverged"}


def build_alignment_prompt(case, response_text, template):
    case_context = build_candidate_prompt(case)
    historical_decision = case["analysis_only"]["historical_decision"].strip()

    return (
        "{}\n\n---\n\nSCENARIO AND QUESTION:\n\n{}\n\n---\n\n"
        "CANDIDATE RESPONSE:\n\n{}\n\n---\n\nHISTORICAL DECISION:\n\n{}\n"
    ).format(template.strip(), case_context, response_text.strip(), historical_decision)


def parse_alignment_output(text):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("No JSON object found in alignment judge output: {!r}".format(text[:200]))
    parsed = json.loads(match.group(0))
    if parsed.get("alignment") not in VALID_ALIGNMENTS:
        raise ValueError("Invalid alignment value: {!r}".format(parsed.get("alignment")))
    return parsed
