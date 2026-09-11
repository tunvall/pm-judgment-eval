# Blind PM validation

## What this checks

The eval's rubrics were all written by one person (Fredrik), who in every
case already knew how the real decision turned out before writing the
grading criteria. `docs/methodology.md`'s hindsight-bias process guards
against smuggling the *answer* into the rubric, but it can't rule out
smuggling in the *author's own reasoning style* — the specific things one
experienced PM happens to weigh, dressed up as "what good judgment looks
like" in general.

This experiment checks that directly: do independent PMs, who've never seen
the rubric, the historical decision, or any model's answer, converge on
roughly the same criteria on their own? If yes, the rubrics have real
construct validity. If no, that's not a failure — it's a finding, and it
changes what the project can honestly claim to measure.

## What's in this folder

- `cases/*.md` — 6 sealed case packets (`escalate-legal-risk` was withdrawn
  entirely from the project — privileged/confidential legal material, not
  usable in any form). Each has only the scenario, the
  question, and the stated constraints. No rubric, no dimensions, no
  historical decision, no model answers. Generated directly from the same
  case files the actual eval uses, so what a PM reads here is exactly what a
  candidate model reads.
- `response-template.md` — the 3 questions each participant answers per
  case.
- `comparison-template.md` — fill this in yourself after responses come
  back, to compare each PM's stated criteria against the existing rubric.

## How to run it

1. **Recruit 2-3 PMs** who have never seen this project, this repo, or
   talked to you about the underlying decisions. Ideally people with real
   product experience, not necessarily senior — the point is independent
   judgment, not a specific seniority bar.
2. **Send each of them the `cases/` folder and `response-template.md`
   only.** Don't send this README, `comparison-template.md`, or anything
   from `evals/`, `docs/methodology.md`, or the blog drafts — anything that
   describes what the "right" answer looks like defeats the purpose.
3. **Have them work independently.** No group discussion until everyone's
   submitted. If two PMs compare notes before finishing, you've lost the
   independence that makes this meaningful.
4. **Collect their answers**, then fill in `comparison-template.md`
   yourself, case by case.
5. **Read the results honestly.** If PMs keep naming criteria you already
   have, that's real signal the rubrics generalize. If they say things like
   "why does X matter so much" about a criterion you weighted heavily, or
   name something essential that isn't in your rubric at all, that's the
   more valuable outcome — it tells you exactly where the rubric reflects
   your own style rather than a broader standard.

## What NOT to do

- Don't cherry-pick which PM responses to report. If 1 of 3 disagrees
  sharply, that's part of the result, not noise to discard.
- Don't rewrite the rubric to match PM feedback and call the experiment
  "validated" — a rubric that changes after seeing this data needs a version
  bump and an honest note, same as every other rubric change in this
  project. This is a check, not a tuning pass.
- Don't run this with people who report to you or who you've discussed AI
  eval work with recently — independence is the entire point.
