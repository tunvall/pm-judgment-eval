# Methodology

This document records the methodological decisions locked in after the Phase 0 design review of SPEC.md, and the process discipline that keeps the benchmark honest as it grows. It is the working reference for how cases get written and scored — SPEC.md is the original design document and is not edited after the fact; corrections and refinements live here and in `docs/learnings.md`.

## What this project measures

This project does not measure "product judgment." It measures performance on seven proxies — ambiguity handling, evidence quality, restraint, tradeoff reasoning, conviction, calibration, and execution practicality — that are a working hypothesis about what product judgment decomposes into. The proxies may turn out to be redundant, incomplete, or unreliable to score. Discovering that is a legitimate outcome of this project, not a failure of it. Any summary of results should describe performance in terms of these named dimensions, not claim to have measured "judgment" as an unqualified construct.

Two dimensions in particular are watched for collapsing into each other rather than assumed distinct from the start: restraint and tradeoffs (not building is itself a tradeoff choice), and conviction and calibration (a well-calibrated model should sometimes defer, so the two will correlate on some cases by design, not by measurement failure). Where a case scores identically on both, that is itself a note-worthy finding, not a bug — see `docs/learnings.md`.

## Historical decision ≠ ground truth

The rubric never scores agreement with what was actually decided. "Fredrik's decision = correct answer" is explicitly rejected as a scoring model. A case's rubric scores reasoning quality against the situation as it was known at decision time; the historical decision and eventual outcome are stored in each case's `analysis_only` block, are programmatically excluded from any prompt shown to a candidate model, and are used only for human/judge analysis after scoring.

## Writing a rubric without hindsight bias

A rubric is written after the case author already knows how the decision turned out, which creates an obvious risk: criteria that quietly reverse-engineer the known-good answer instead of testing whether the *reasoning* was sound given contemporaneous information.

Process for every case:

1. Draft `scenario`, `information_available_at_the_time`, `constraints`, and `question` first, from the case's non-`analysis_only` fields only.
2. Write the rubric criteria against that draft, without rereading `analysis_only.historical_decision` or `analysis_only.eventual_outcome` while writing.
3. Only after the rubric is drafted, reread the outcome and sanity-check: does the rubric miss something the outcome revealed was actually decision-relevant at the time? If so, add it as a criterion grounded in the *contemporaneous* information, not the outcome itself.

This is a discipline, not a schema enforcement — nothing in the case file format prevents skipping it. Treat it as part of what "done" means for a case.

## Sanitization must not erase the hard part

Abstracting a case for the repo risks removing exactly the domain-specific detail that made the decision non-obvious, leaving a generic scenario any model gets right or wrong for reasons unrelated to judgment. After sanitizing a case, reread it cold and ask: would a smart person unfamiliar with the original situation still find this decision genuinely hard, with a real chance of choosing wrong? If the sanitized version reads as obvious, it has been abstracted past the point of being useful — cut it rather than keep it for case count. (Full sanitization checklist lives outside this repo — see the note at the bottom of this file.)

## Trials per case

Each case is run at least **2 times per model** before its score is treated as meaningful. Model output is stochastic; a single run cannot distinguish "this model is weak on this dimension" from "this model got unlucky on one generation." The run/results data model keys on `case_id × model × trial`, not `case_id × model`.

## System prompt and harness scope

The core benchmark tests models, not harnesses. Every model receives an identical, minimal system prompt — no vendor-specific tuning, and no personal skills, style guides, or CLAUDE.md-style customization applied to any one vendor and not the others. Applying custom instruction tuning to one model (e.g. Claude, under a personally-developed skills setup) while testing others out of the box would compare "a heavily prompt-engineered model" against "vanilla everyone else," which confounds prompt-engineering effort with model capability and makes any result uninterpretable.

If there's a later interest in testing whether a specific personal setup (e.g. a Claude Code configuration with custom skills) measurably improves judgment scores over the vanilla model, that is a distinct, explicitly-labeled Phase 7 harness experiment — reported separately, never blended into the core model-vs-model comparison.

## Scoring reliability

Not every rubric criterion is equally trustworthy as a numeric score. Criteria that ask whether a specific, checkable thing was done or mentioned (e.g. "proposes a realistic next step") are more reliably judge-scorable than criteria that ask whether a stance was *correct* (e.g. "conviction" scored as "did it disagree" risks collapsing back into agreement-with-Fredrik scoring through the back door). Where a criterion can't be scored without smuggling in agreement with the historical decision, it should be flagged as qualitative-only in the case file and excluded from any weighted aggregate, even if it's still worth reading in raw judge output.

Rubric weights are provisional until the first 5-case run produces actual scoring behavior to look at. Do not treat a weight of `3` as more precise than "this criterion matters somewhat more than a `2`."

## Anti-verbosity, anti-hedging

The judge prompt must explicitly instruct against two specific gaming patterns: rewarding length or exhaustiveness (e.g. a criterion like "identifies the core uncertainty" satisfied by listing five plausible uncertainties rather than identifying the one that actually matters), and rewarding hedge-everything answers that never commit to a recommendation. A model that lists every consideration and commits to nothing should score worse on tradeoff and conviction criteria than a model that reasons to a specific call, even if the hedged answer is longer and touches more of the rubric's surface area.

## Reporting

No single aggregate leaderboard score is the primary output of an evaluation run. Primary outputs are per-dimension performance, case-level disagreement between models, judge-vs-human disagreement, and specific strong/weak response examples. A total score may be computed but is secondary to the qualitative comparison.

## Cost and efficiency

Cost is tracked as a separate reported axis, never folded into the judgment-dimension scores or any weighted aggregate. Raw token counts are not compared directly across vendors — each provider (Anthropic, OpenAI, Google, Mistral, xAI, etc.) uses its own tokenizer, so the same response text yields a different token count depending on which model produced it, making cross-vendor token counts an apples-to-oranges comparison.

Instead: read `input_tokens`/`output_tokens` directly from each API response's usage metadata (every major provider returns this — no local tokenizer needed), then multiply by that provider's published per-token rate to get actual dollar cost per response. This is the real per-unit-cost proxy. Report it alongside judgment scores as a comparison (e.g. "Model A scores highest on tradeoff reasoning but costs 3x more per response than Model B, which scores nearly as well"), not blended into a single number.

Latency (wall-clock time per response) is logged as free metadata captured from timing each API call, but is not a scored dimension in v0 — secondary to cost, worth having recorded, not worth building analysis around yet.

## Repeatability across model releases

A core design goal is that testing a newly-released model against the existing results should be cheap and valid, not a full re-run. This requires:

- **The case set, rubric, and judge are frozen before cross-vendor comparison begins**, and versioned (`case_version`, `judge_prompt_version`, already part of the Section 14 run-metadata schema in SPEC.md). A new model's score is only comparable to existing scores if it was evaluated against the same case version and judge version. If a case needs to change later, that's a new case version, and any comparison spanning the change carries a caveat rather than being treated as apples-to-apples.
- **Results are append-only.** The results store is keyed by `case_id × model × trial × run_id`. Testing a new model means running only that model against the frozen case set and appending — never re-running models already on the board. The reporting step recomputes the comparison from whatever is currently in the store, so it can be rerun at any time to pick up newly-added models.
- **Model versions are pinned exactly**, never referenced by a rolling alias like "latest" — providers update what an alias points to without warning, which would silently break reproducibility for exactly this workflow. The exact pinned model ID is recorded in run metadata (`model_version_if_known`).
- **The judge is the fragile point in this chain.** Upgrading the judge model invalidates comparability between scores produced under the old judge and the new one, since the standard being applied changed, not just the model being tested. Judge changes should be rare and deliberate: bump `judge_prompt_version` when it happens, and re-judge a sample of already-scored models under the new judge to see how much rankings shift, following the same judge-reliability check already described for LLM-as-judge generally.

## Truncation is a fairness risk, not just a data-quality one

The default `max_tokens` (4096) is not equally generous across every
model/layer combination. `claude-fable-5-1` under the structured layer hit
exactly 4096 output tokens on `terminology-never-landed`, mid-sentence,
confirmed by inspecting the raw response text, not inferred from the token
count alone. A truncated response scored against the rubric as-is would be
penalized for an infrastructure limit, not for its actual reasoning; a
criterion like a required "next steps" section could score not_met simply
because the response never got there, which is a fairness violation on top
of the more familiar "no ambiguity" quality-of-run issue.

Handled by re-running that specific call at double the budget (8192) and
confirming by inspection that the new response ends naturally. Not fixed
generally: `max_tokens` is still 4096 by default. Two other Fable 5.1
structured responses landed at 3643 and 3691 tokens, close to the ceiling
but confirmed complete by inspection, meaning this model/layer combination
runs close to the edge routinely, not just in this one instance. Worth
raising the default for structured-layer runs specifically before running
this at any larger scale, and worth spot-checking any future response whose
output_tokens lands suspiciously close to whatever ceiling is set, the same
discipline used here, not just trusting the token count.

## Flagship selection was inconsistent across vendors, now corrected

The original "one strong model per vendor" line-up (Phase 5) was `claude-sonnet-5`,
`gpt-5.6-sol`, `gemini-3.1-pro-preview`. The OpenAI and Gemini picks were verified
against each vendor's own documentation as their actual flagship at the time.
`claude-sonnet-5` was not verified the same way; it was chosen because it happened
to be the model running this project, not because it was confirmed to be
Anthropic's top tier. It is not: Anthropic's flagship line at the time was
`claude-fable-5-1` (Mythos-class, positioned above Opus-class, itself above
Sonnet). This means every comparative result produced before this correction had
Claude represented by a mid-tier model while the other two vendors were
represented by their actual best. That is a real, uncorrected asymmetry in past
results, not a minor caveat — any conclusion drawn from data before this point
that compares Claude's standing against GPT or Gemini should be treated as
comparing the wrong tier, not a fair three-way flagship comparison.

Corrected line-up: `claude-fable-5-1`, `gpt-6-astra`, `gemini-3.1-pro-preview`.
GPT-5.6-Sol was itself superseded by GPT-6 Astra five days after this project
started using it; Gemini's pick was rechecked at the same time and remains
current (Google's next Pro-tier model had not shipped as of this check).

Two things worth naming about the corrected models rather than treating the
fix as complete and moving on:

- `claude-fable-5-1` and `gpt-6-astra` are both built and marketed primarily
  for sustained, multi-step agentic work (planning across stages, tool use,
  long-horizon tasks), not single-shot Q&A. That's not disqualifying for this
  project's stateless single-turn calls, but it means both models are being
  used somewhat outside their headline use case, worth remembering when
  interpreting results.
- Both models carry safety-classifier behavior that can silently reroute or
  refuse certain sensitive request categories (cybersecurity, bio/chem,
  model distillation). None of this project's cases should trigger that, but
  it means the model ID alone doesn't unconditionally guarantee that model
  answered every call; worth spot-checking if a response ever looks anomalous.

Practical lesson for adding any future vendor or re-checking an existing one:
verify the current flagship via the vendor's own docs or a live model-list
query, every time, regardless of which model happens to be convenient (e.g.,
being the model already running the project). Convenience was exactly how
this asymmetry got introduced in the first place.

## Dev set vs. held-out set

Every case has a `set` field: `dev` or `heldout`. The distinction matters and was
not explicit until a later methodology review caught that it should be: the
original 5 cases were used to validate the schema, the rubric-writing process, and
the judge, including reading real scored Claude output while building confidence
in the mechanism. That makes them a development set, not a clean comparison set,
even though nothing was tuned dishonestly against them.

Held-out cases are converted from the sanitized shortlist the same way as dev
cases, following the same hindsight-bias rubric process, but are never viewed
against any model's real output before being finalized. Comparative conclusions
about model behavior should be drawn primarily from held-out results; dev-set
results are useful for continuity and sanity-checking but should be reported
separately, never blended into the same leaderboard.

## Iteration sequencing across vendors

Case set, rubric, and judge get iterated against a single model family first (not the full vendor set) — cheaper and faster to develop against one API while the schema and rubric are still unstable. Only once the rubric and judge are stable does the frozen v1 dataset run against the broader vendor set (Phase 5).

Risk to watch during iteration: developing the rubric primarily against one vendor's outputs risks shaping it — not around the "correct" answer (that risk is already handled by the hindsight-bias process above), but around that vendor's typical response *style* — its structure, hedging patterns, verbosity — in ways that could unfairly penalize a differently-shaped but equally valid response from another vendor. Before calling the rubric final, sanity-check 2-3 cases against a second model (a spot check, not a full run) specifically to confirm the rubric doesn't silently reward or punish stylistic patterns rather than reasoning quality.

## Judge validation: does the rubric actually discriminate

Near-ceiling scores across a real candidate model's outputs are not, by themselves,
evidence that the judge or rubric works. They could equally mean the rubric is too
easy to satisfy. Before trusting scores from any rubric/judge pair, check that a
deliberately weak response scores meaningfully lower than the real candidate
outputs on the same case. `tests/fixtures/adversarial-hedge-test.json` is a
hand-written, intentionally hedging, non-committal answer to the `private-nudge`
case, run through `src/score.py` the same way a real result would be. First run:
2.5/10 versus 10/10 for the real candidate outputs on that case, with justifications
that correctly identified the specific hedging pattern (never naming the actual
deadline fact, never committing to an action, listing the public-channel option
without scrutinizing it).

That check only tests one direction: does the judge punish an obviously weak
answer. It doesn't test whether the judge is actually scoring reasoning, or just
pattern-matching on the candidate model's typical writing style. All real v0
outputs came from the same model, so they share a style (long, structured, bold
headers, self-explaining). `tests/fixtures/known-good-terse-test.json` is a
hand-written answer to the same case, deliberately terse and blunt, no headers, no
elaboration, but substantively hitting every rubric criterion. It also scored
10/10, with justifications quoting the terse phrasing directly rather than
defaulting to boilerplate. Together, both fixtures are evidence the rubric can
discriminate on substance in both directions, rewarding a good answer regardless of
style and punishing a bad one regardless of length. Neither fixture is evidence
that self-preference bias is absent, since the same model was candidate and judge
for both. That question stays open until a second model exists to judge with
(Phase 5).

## A note on where the sanitization/NDA process lives

The step-by-step checklist for what can and cannot leave the internal environment, and the pre-commit review process for sanitized cases, is deliberately kept outside this repository so it never ships even if this repo eventually goes public. It is referenced here only as: consult that checklist before adding or updating any case sourced from real work history.
