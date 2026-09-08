"""CLI: score decision alignment for one saved run against its case's historical
decision. Kept separate from src/score.py; see src/alignment.py for why.
"""

import argparse
import json
import subprocess
import uuid
from datetime import datetime, timezone
from pathlib import Path

from src.alignment import ALIGNMENT_PROMPT_VERSION, build_alignment_prompt, parse_alignment_output
from src.case_loader import load_case
from src.models import PROVIDERS

ALIGNMENT_PROMPT_PATH = Path("prompts/judge/alignment-prompt-v1.md")


def get_git_commit():
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()
    except Exception:
        return None


def score_alignment(run_path, judge_provider, judge_model, temperature=None, max_retries=1):
    run_record = json.loads(Path(run_path).read_text())
    case = load_case("evals/cases/{}.yaml".format(run_record["case_id"]))

    template = ALIGNMENT_PROMPT_PATH.read_text()
    prompt = build_alignment_prompt(case, run_record["response"], template)
    call_fn = PROVIDERS[judge_provider]

    score_id = "{}__alignment-{}__{}".format(run_record["run_id"], judge_model, uuid.uuid4().hex[:8])
    base_record = {
        "score_id": score_id,
        "run_id": run_record["run_id"],
        "case_id": run_record["case_id"],
        # See src/score.py for why this is the case's current version, not the
        # run's original case_version: it records which historical_decision
        # text was actually compared against, which can be revised
        # independently of the candidate's original run.
        "case_version": case["version"],
        "candidate_case_version": run_record["case_version"],
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "git_commit": get_git_commit(),
        "judge_provider": judge_provider,
        "judge_model": judge_model,
        "alignment_prompt_version": ALIGNMENT_PROMPT_VERSION,
    }

    scores_dir = Path("scores_alignment")
    scores_dir.mkdir(exist_ok=True)

    last_error = None
    for attempt in range(max_retries + 1):
        judge_response = call_fn(model=judge_model, system_prompt="", user_prompt=prompt, temperature=temperature)
        try:
            parsed = parse_alignment_output(judge_response.text)
        except (ValueError, KeyError) as e:
            last_error = str(e)
            continue

        record = dict(base_record, alignment=parsed["alignment"],
                      justification=parsed.get("justification", ""), raw_judge_response=judge_response.text)
        out_path = scores_dir / "{}.json".format(score_id)
        out_path.write_text(json.dumps(record, indent=2))
        return record, out_path

    failed_record = dict(base_record, failed=True, error=last_error)
    out_path = scores_dir / "{}__FAILED.json".format(score_id)
    out_path.write_text(json.dumps(failed_record, indent=2))
    return failed_record, out_path


def main():
    parser = argparse.ArgumentParser(description="Score decision alignment for one saved run.")
    parser.add_argument("--run", required=True)
    parser.add_argument("--judge-provider", default="anthropic")
    parser.add_argument("--judge-model", required=True)
    parser.add_argument("--temperature", type=float, default=None)
    args = parser.parse_args()

    record, out_path = score_alignment(args.run, args.judge_provider, args.judge_model, args.temperature)
    print("Saved: {}".format(out_path))
    if record.get("failed"):
        print("FAILED after retries: {}".format(record["error"]))
        return
    print("Alignment: {}".format(record["alignment"]))
    print("Justification: {}".format(record["justification"]))


if __name__ == "__main__":
    main()
