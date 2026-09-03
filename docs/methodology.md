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

## Scoring reliability

Not every rubric criterion is equally trustworthy as a numeric score. Criteria that ask whether a specific, checkable thing was done or mentioned (e.g. "proposes a realistic next step") are more reliably judge-scorable than criteria that ask whether a stance was *correct* (e.g. "conviction" scored as "did it disagree" risks collapsing back into agreement-with-Fredrik scoring through the back door). Where a criterion can't be scored without smuggling in agreement with the historical decision, it should be flagged as qualitative-only in the case file and excluded from any weighted aggregate, even if it's still worth reading in raw judge output.

Rubric weights are provisional until the first 5-case run produces actual scoring behavior to look at. Do not treat a weight of `3` as more precise than "this criterion matters somewhat more than a `2`."

## Anti-verbosity, anti-hedging

The judge prompt must explicitly instruct against two specific gaming patterns: rewarding length or exhaustiveness (e.g. a criterion like "identifies the core uncertainty" satisfied by listing five plausible uncertainties rather than identifying the one that actually matters), and rewarding hedge-everything answers that never commit to a recommendation. A model that lists every consideration and commits to nothing should score worse on tradeoff and conviction criteria than a model that reasons to a specific call, even if the hedged answer is longer and touches more of the rubric's surface area.

## Reporting

No single aggregate leaderboard score is the primary output of an evaluation run. Primary outputs are per-dimension performance, case-level disagreement between models, judge-vs-human disagreement, and specific strong/weak response examples. A total score may be computed but is secondary to the qualitative comparison.

## A note on where the sanitization/NDA process lives

The step-by-step checklist for what can and cannot leave the internal environment, and the pre-commit review process for sanitized cases, is deliberately kept outside this repository so it never ships even if this repo eventually goes public. It is referenced here only as: consult that checklist before adding or updating any case sourced from real work history.
