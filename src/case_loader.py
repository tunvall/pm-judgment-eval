"""Load case YAML files and build the candidate-facing prompt.

The candidate prompt is built by allowlisting specific fields (title, scenario,
question, constraints). analysis_only is never read here, so it cannot leak into
the prompt through this path. tests/test_prompt_exclusion.py checks this directly
against every case file as a second, independent safeguard.
"""

from pathlib import Path

import yaml

CANDIDATE_FIELDS = ("title", "scenario", "question", "constraints")


def load_case(path):
    with open(path) as f:
        return yaml.safe_load(f)


def load_all_cases(cases_dir="evals/cases"):
    return [load_case(p) for p in sorted(Path(cases_dir).glob("*.yaml"))]


def build_candidate_prompt(case):
    lines = [f"# {case['title']}", "", case["scenario"].strip(), "", case["question"].strip()]

    constraints = case.get("constraints")
    if constraints:
        lines.append("")
        lines.append("Constraints:")
        for c in constraints:
            lines.append(f"- {c}")

    return "\n".join(lines)
