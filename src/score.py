"""CLI: score one saved run against its case's rubric using a judge model."""

import argparse
import json
import subprocess
import uuid
from datetime import datetime, timezone
from pathlib import Path

from src.case_loader import load_case
from src.judge import JUDGE_PROMPT_VERSION, build_judge_prompt, parse_judge_output, score_criteria
from src.models import PROVIDERS

JUDGE_PROMPT_PATH = Path("prompts/judge/judge-prompt-v1.md")


def get_git_commit():
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()
    except Exception:
        return None


def score_run(run_path, judge_provider, judge_model, temperature=None, max_retries=1):
    run_record = json.loads(Path(run_path).read_text())
    case = load_case("evals/cases/{}.yaml".format(run_record["case_id"]))

    template = JUDGE_PROMPT_PATH.read_text()
    judge_prompt = build_judge_prompt(case, run_record["response"], template)
    call_fn = PROVIDERS[judge_provider]

    score_id = "{}__judge-{}__{}".format(run_record["run_id"], judge_model, uuid.uuid4().hex[:8])
    base_record = {
        "score_id": score_id,
        "run_id": run_record["run_id"],
        "case_id": run_record["case_id"],
        "case_version": run_record["case_version"],
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "git_commit": get_git_commit(),
        "judge_provider": judge_provider,
        "judge_model": judge_model,
        "judge_prompt_version": JUDGE_PROMPT_VERSION,
    }

    scores_dir = Path("scores")
    scores_dir.mkdir(exist_ok=True)

    last_error = None
    for attempt in range(max_retries + 1):
        judge_response = call_fn(model=judge_model, system_prompt="", user_prompt=judge_prompt, temperature=temperature)
        try:
            judge_output = parse_judge_output(judge_response.text)
            scored_criteria, weighted_sum, max_possible = score_criteria(case, judge_output)
        except (ValueError, KeyError) as e:
            last_error = str(e)
            base_record["raw_judge_response"] = judge_response.text
            continue

        record = dict(base_record, criteria=scored_criteria, weighted_total=weighted_sum,
                      max_possible=max_possible, raw_judge_response=judge_response.text)
        out_path = scores_dir / "{}.json".format(score_id)
        out_path.write_text(json.dumps(record, indent=2))
        return record, out_path

    # Every attempt failed to parse. Save a failed record rather than crash and
    # lose the fact that this happened; see docs/methodology.md on reliability.
    failed_record = dict(base_record, failed=True, error=last_error)
    out_path = scores_dir / "{}__FAILED.json".format(score_id)
    out_path.write_text(json.dumps(failed_record, indent=2))
    return failed_record, out_path


def main():
    parser = argparse.ArgumentParser(description="Score one saved run against its case's rubric.")
    parser.add_argument("--run", required=True, help="Path to a saved result JSON file")
    parser.add_argument("--judge-provider", default="anthropic")
    parser.add_argument("--judge-model", required=True)
    parser.add_argument("--temperature", type=float, default=None,
                         help="Omit to use the API's own default; some model versions reject temperature=0.")
    args = parser.parse_args()

    record, out_path = score_run(args.run, args.judge_provider, args.judge_model, args.temperature)
    print("Saved: {}".format(out_path))
    if record.get("failed"):
        print("FAILED after retries: {}".format(record["error"]))
        return
    print("Weighted: {:.2f} / {:.2f}".format(record["weighted_total"], record["max_possible"]))
    for c in record["criteria"]:
        print("  [{}] {} (weight {})".format(c["verdict"], c["id"], c["weight"]))


if __name__ == "__main__":
    main()
