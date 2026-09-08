"""Reporting: aggregate results/, scores/, and scores_alignment/ into one readable
view, grouped by case/model/layer, with dev vs. heldout split and judge
disagreement flagged directly. Reads only already-committed data; makes no API
calls, so it's free and safe to run as often as useful.
"""

import json
from collections import defaultdict
from pathlib import Path

from src.case_loader import load_all_cases

# Hand-written test fixtures, not real model runs; excluded from the report.
EXCLUDE_RUN_IDS = {"adversarial-hedge-test", "known-good-terse-test"}


def load_case_sets():
    return {c["id"]: c.get("set", "unknown") for c in load_all_cases()}


def load_json_dir(path):
    items = []
    if not Path(path).exists():
        return items
    for f in sorted(Path(path).glob("*.json")):
        try:
            items.append(json.loads(f.read_text()))
        except json.JSONDecodeError:
            continue
    return items


def build_report():
    case_sets = load_case_sets()

    runs = {
        r["run_id"]: r for r in load_json_dir("results") if r["run_id"] not in EXCLUDE_RUN_IDS
    }

    reasoning_scores = defaultdict(list)
    for s in load_json_dir("scores"):
        if s.get("failed"):
            continue
        if s.get("run_id") in runs:
            reasoning_scores[s["run_id"]].append(s)

    alignment_scores = defaultdict(list)
    for s in load_json_dir("scores_alignment"):
        if s.get("failed"):
            continue
        if s.get("run_id") in runs:
            alignment_scores[s["run_id"]].append(s)

    rows = []
    for run_id, run in runs.items():
        case_id = run["case_id"]
        row = {
            "case_id": case_id,
            "set": case_sets.get(case_id, "unknown"),
            "model": run["model_name"],
            "layer": run.get("layer", "zero-shot"),
            "trial": run.get("trial", 1),
            "reasoning": [(s["judge_model"], s["weighted_total"], s["max_possible"])
                          for s in reasoning_scores.get(run_id, [])],
            "alignment": [(s["judge_model"], s["alignment"]) for s in alignment_scores.get(run_id, [])],
        }
        rows.append(row)

    return rows


def format_report(rows):
    rows = sorted(rows, key=lambda r: (r["set"], r["case_id"], r["layer"], r["model"], r["trial"]))
    lines = []

    for r in rows:
        reasoning_str = "; ".join(
            "{}: {:.1f}/{:.1f}".format(j, s, m) for j, s, m in r["reasoning"]
        ) or "not scored"
        alignment_str = "; ".join(
            "{}: {}".format(j, a) for j, a in r["alignment"]
        ) or "not scored"

        flags = []
        if len(r["reasoning"]) > 1:
            ratios = {round(s / m, 2) if m else 0 for _, s, m in r["reasoning"]}
            if len(ratios) > 1:
                flags.append("REASONING JUDGES DISAGREE")
        if len(r["alignment"]) > 1:
            verdicts = {a for _, a in r["alignment"]}
            if len(verdicts) > 1:
                flags.append("ALIGNMENT JUDGES DISAGREE")
        flag_str = "  <<< " + ", ".join(flags) if flags else ""

        lines.append(
            "[{set}] {case_id} | {model} | {layer} | trial {trial}\n"
            "  reasoning: {reasoning}\n"
            "  alignment: {alignment}{flag}".format(
                set=r["set"], case_id=r["case_id"], model=r["model"], layer=r["layer"],
                trial=r["trial"], reasoning=reasoning_str, alignment=alignment_str, flag=flag_str,
            )
        )

    return "\n\n".join(lines)


def main():
    rows = build_report()
    print(format_report(rows))
    print()
    print("Total runs: {}".format(len(rows)))
    print("Scored (reasoning): {}  Scored (alignment): {}".format(
        sum(1 for r in rows if r["reasoning"]), sum(1 for r in rows if r["alignment"])
    ))


if __name__ == "__main__":
    main()
