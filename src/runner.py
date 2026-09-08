"""Minimal runner: load a case, build the candidate prompt, call one model, persist
the raw result with full run metadata. See docs/methodology.md for why each of
these fields is captured (case_version and model pinning make results comparable
across time; token usage from the API response, not a local tokenizer, makes cost
comparable across vendors).
"""

import argparse
import json
import subprocess
import uuid
from datetime import datetime, timezone
from pathlib import Path

from src.case_loader import build_candidate_prompt, load_case
from src.models import PROVIDERS

LAYERS = {
    "zero-shot": {
        "path": Path("prompts/candidate/system-prompt-v1.md"),
        "version": "v1",
    },
    "structured": {
        "path": Path("prompts/candidate/system-prompt-structured-v1.md"),
        "version": "structured-v1",
    },
}

# Forced identical across providers for candidate calls, so "randomness level" is a
# controlled variable in cross-model comparisons, not just the request shape. See
# docs/methodology.md for why this was made an explicit decision rather than left
# as each provider's undocumented default.
DEFAULT_TEMPERATURE = 1.0
DEFAULT_MAX_TOKENS = 4096


def get_git_commit():
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()
    except Exception:
        return None


def run(case_path, provider, model, trial=1, temperature=DEFAULT_TEMPERATURE, max_tokens=DEFAULT_MAX_TOKENS,
        layer="zero-shot"):
    case = load_case(case_path)
    user_prompt = build_candidate_prompt(case)
    layer_spec = LAYERS[layer]
    system_prompt = layer_spec["path"].read_text()

    call_fn = PROVIDERS[provider]
    response = call_fn(
        model=model, system_prompt=system_prompt, user_prompt=user_prompt,
        temperature=temperature, max_tokens=max_tokens,
    )

    run_id = "{}__{}__{}__t{}__{}".format(case["id"], model, layer, trial, uuid.uuid4().hex[:8])

    record = {
        "run_id": run_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "git_commit": get_git_commit(),
        "case_id": case["id"],
        "case_version": case["version"],
        "trial": trial,
        "layer": layer,
        "model_provider": provider,
        "model_name": model,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "system_prompt_version": layer_spec["version"],
        "input_tokens": response.input_tokens,
        "output_tokens": response.output_tokens,
        "latency_ms": response.latency_ms,
        "prompt": user_prompt,
        "response": response.text,
    }

    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)
    out_path = results_dir / "{}.json".format(run_id)
    out_path.write_text(json.dumps(record, indent=2))

    return record, out_path


def main():
    parser = argparse.ArgumentParser(description="Run one case against one model.")
    parser.add_argument("--case", required=True, help="Path to a case YAML file")
    parser.add_argument("--provider", default="anthropic", choices=list(PROVIDERS.keys()))
    parser.add_argument("--model", required=True, help="Exact pinned model version string, never an alias")
    parser.add_argument("--trial", type=int, default=1)
    parser.add_argument("--temperature", type=float, default=DEFAULT_TEMPERATURE,
                         help="Forced identical across providers for fair comparison; override only for debugging.")
    parser.add_argument("--max-tokens", type=int, default=DEFAULT_MAX_TOKENS)
    parser.add_argument("--layer", default="zero-shot", choices=list(LAYERS.keys()))
    args = parser.parse_args()

    record, out_path = run(args.case, args.provider, args.model, args.trial, args.temperature,
                            args.max_tokens, args.layer)
    print("Saved: {}".format(out_path))
    print("Input tokens: {}  Output tokens: {}  Latency: {}ms".format(
        record["input_tokens"], record["output_tokens"], record["latency_ms"]
    ))


if __name__ == "__main__":
    main()
