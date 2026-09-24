# Model expansion run plan (proposed, not yet executed)

Written 2026-09-24, in response to new model releases from Anthropic and
OpenAI mid-project. This document is the proposal to review before any new
API calls are made. See `docs/methodology.md` for the standing principles
this plan applies (frozen judges, pinned model versions, honest limitations).

## Audit of the current experiment (verified against the live repo)

- **11 cases** (6 dev, 5 held-out), each with a rubric and a stored
  historical decision.
- **5 existing candidates**: `claude-sonnet-5`, `claude-fable-5-1`,
  `gpt-5.6-sol`, `gpt-6-astra`, `gemini-3.1-pro-preview`. All 5 have full
  coverage across all 11 cases, zero-shot format, at least 1 trial; several
  also have a 2nd zero-shot trial and a structured-prompt trial.
- **3 reasoning judges** (`claude-sonnet-5`, `gpt-5.6-sol`,
  `gemini-3.1-pro-preview`) score every candidate response independently,
  this is what caught the self-preference effect.
- **1 primary alignment judge** (`claude-sonnet-5`, 103 of 128 alignment
  scores; a handful of early scores used the other two, not a settled
  practice) checks the candidate's decision against history, completely
  separately from the reasoning judges.
- **Reasoning-effort/thinking parameters were never set on any candidate
  call.** `temperature` and `max_tokens` are the only parameters the runner
  controls, and even `temperature` gets silently dropped on models that
  reject it (see `src/models.py`'s deprecation handling).
- `max_tokens` is 4096 for 94 of 103 existing results, with 8 outliers at
  unset/None (all `claude-sonnet-5`) and 1 at 8192 (`claude-fable-5-1`), a
  small pre-existing wrinkle, noted rather than silently treated as
  perfectly uniform.

## Should judges stay frozen while adding new candidates?

Yes. This isn't a new judgment call, it's the project's own already-written
principle: "The case set, rubric, and judge are frozen before cross-vendor
comparison begins... upgrading the judge model invalidates comparability
between scores produced under the old judge and the new one, since the
standard being applied changed, not just the model being tested"
(`docs/methodology.md`). Changing the judge while adding new candidates
would confound "is this a better model" with "is this a different rubric
interpretation."

**Real nuance this expansion surfaces**: the existing self-preference
finding is defined at the exact-model level (does `gpt-5.6-sol`-as-judge
favor `gpt-5.6-sol`-as-candidate specifically). None of the 3 new candidates
are also judges, so this addition produces no new *exact* self-preference
data point, only new "judge scores a different vendor's model" data. The
self-preference table's existing conclusion (Claude's judge shows a real
+3.2 gap, GPT and Gemini don't) doesn't change from this addition alone,
though the composition of "other" responses judges are compared against
does grow, and the per-case and aggregate tables need a full recompute
regardless once new candidates enter the dataset.

## New models and their API IDs

| Vendor | Model | Positioning (per vendor's own materials) |
|---|---|---|
| Anthropic | `claude-opus-5-5` | Confirmed via Anthropic's own model catalog: Opus tier sits below Fable in capability, roughly half Fable's price. Newest Anthropic release as of this writing, but not a new top tier. |
| OpenAI | `gpt-6-sol` | Per OpenAI's own launch announcement: "built around complex coding and agentic workflows while balancing capability and cost" — a cheaper Astra-architecture derivative, not a replacement. |
| OpenAI | `gpt-6-luna` | Per the same announcement: "the most efficient option for focused, high-volume tasks" — the cheapest of the three. |

`gpt-6-astra` remains the confirmed flagship (unchanged, already in the
dataset). No newer Anthropic top-tier model exists as of this writing;
`claude-fable-5-1` remains the flagship.

## Reasoning-effort configuration, checked per API, not assumed

- **Anthropic**: controlled via `output_config.effort`
  (`low`/`medium`/`high`/`xhigh`/`max`), defaults to `high` if omitted.
  `claude-fable-5-1`'s thinking is always on with no way to disable it below
  `xhigh`/`max`; `claude-opus-5-5` inherits Opus 5's behavior (thinking on
  by default, disabling capped at `high` or below).
- **OpenAI**: controlled via `reasoning_effort`, same five-step ladder plus
  a `none` option that fully disables reasoning. Sol and Luna both support
  `none`; unconfirmed whether Astra does.
- **Google**: controlled via `thinking_level`, but on a **four-step** scale
  (`minimal`/`low`/`medium`/`high`), not five, defaulting to `medium`.

**These are not equivalent scales across vendors, and no verified mapping
exists between, say, Anthropic's "medium" and OpenAI's "medium."**

**Recommendation: leave reasoning-effort unset on all 3 new candidates**,
for exact continuity with how the existing 5 were generated (none of them
ever had this parameter set either). This means every model runs at its own
vendor-chosen default, which is not a matched setting across vendors, and
that's named as a real limitation below rather than papered over with a
same-looking label that wouldn't represent equivalent compute anyway.
Holding reasoning-effort constant as a controlled variable is a legitimate
follow-on experiment, but it would require also re-running the existing 5
candidates, which trades away the continuity this plan is built to preserve.

## Proposed run

| | |
|---|---|
| New candidates | `claude-opus-5-5`, `gpt-6-sol`, `gpt-6-luna` |
| Existing candidates | All 5 stay exactly as-is: no re-runs, no re-scoring |
| Cases | All 11, matching the coverage floor every existing candidate already has |
| Trials / format | 1 trial, zero-shot only, per new candidate per case (matches the baseline every existing candidate has; a 2nd trial and structured format are optional follow-ons, not included here) |
| Reasoning settings | Unset on all three, matching every existing candidate |
| Judges scoring new responses | All 3 existing reasoning judges + the existing alignment judge (`claude-sonnet-5`) — full parity with how every existing candidate was scored |
| Existing responses needing rescoring | None |

**Call counts**: 33 new candidate generations (3 models × 11 cases) → 99
reasoning-judge calls (3 judges × 33) → 33 alignment calls = **165 total new
API calls.**

## Estimated cost

Using this project's own real average token usage per call (≈466 input /
≈1,245 output tokens, measured from the existing 103 calls) against real,
sourced current per-token rates:

| | Rate ($/M in, $/M out) | Est. cost |
|---|---|---|
| `claude-opus-5-5` × 11 | $5 / $25 | ~$0.37 |
| `gpt-6-sol` × 11 | $2 / $10 | ~$0.15 |
| `gpt-6-luna` × 11 | $0.10 / $0.50 | ~$0.01 |
| Reasoning judges × 99 (33 per judge) | `gpt-5.6-sol`: $4/$20 confirmed (developers.openai.com/api/docs/models/gpt-5.6-sol); `claude-sonnet-5` and `gemini-3.1-pro-preview` rates still not independently confirmed | ~$0.85, wider error bars on 2 of the 3 judges |
| Alignment judge × 33 | $3 / $15 | ~$0.35 |
| **Total** | | **~$1.70–2.00** |

**Two distinct gaps remain in the judge-cost line, worth naming separately**:
1. `gpt-5.6-sol`'s rate is now confirmed ($4/M input, $20/M output, plus
   $0.4/M cached input and a 2x/1.5x surcharge above 272K input tokens per
   its official docs page), correcting the earlier placeholder. `claude-sonnet-5`
   and `gemini-3.1-pro-preview`'s exact current rates are still unconfirmed.
2. More fundamentally, `src/score.py` never records input/output token
   counts for judge calls at all, unlike `src/runner.py`, which does for
   candidate calls. The candidate-cost figures above are built from real
   measured tokens; the judge-cost figures are a rough approximation
   regardless of rate precision, because the actual token volume per judge
   call was never captured historically. Neither gap moves the total order
   of magnitude (well under $2 either way), but the judge-cost line should
   be read as directionally correct, not precise, until token usage is
   actually captured on judge calls going forward.

## Comparability limitations, stated plainly

1. Reasoning effort is uncontrolled across all 8 models, old and new alike.
   A "best model" finding here is "best model at its own default effort,"
   not at matched effort across vendors.
2. New candidates get 1 trial only, so no reliability class
   (stable/drift/unstable) can be computed for them this pass, unlike some
   existing candidates.
3. `gpt-6-sol` is a genuinely different, newer model from the
   already-present `gpt-5.6-sol` — worth deliberately not conflating the
   two when reading results.
4. `claude-opus-5-5` and `claude-fable-5-1`'s pricing is inherited from
   their base generation's published rate (Anthropic prices at the
   generation level, not the point release) — a reasonable inference, not a
   directly confirmed number for the exact dot-release ID.

## What needs regenerating vs. what's genuinely new

- **Regenerate**: per-case results table, aggregate rankings (both need the
  3 new rows added).
- **Genuinely new, not a regeneration**: the cost comparison and the
  quality/cost frontier, this project has never tracked real dollar cost
  before now.
- **Unaffected, no change needed**: the self-preference table (no new
  exact-match judge/candidate pair exists), format-sensitivity findings
  (new candidates aren't run structured), temperature-sensitivity findings
  (new candidates aren't run at alternate temperatures), historical-alignment
  findings for the existing 5 candidates.

## Status

Proposed, not executed. Awaiting review.
