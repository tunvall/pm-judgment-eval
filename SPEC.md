# Product Judgment Eval — Project Spec and Build Plan

**Working title:** `pm-judgment-eval`  
**Status:** v0 planning / pre-implementation  
**Primary builder:** Fredrik, using Claude CLI as the local coding partner  
**Primary purpose:** Build a small, credible evaluation system that tests how AI models/products reason through real product-management decisions, while giving Fredrik hands-on experience with spec-driven development, evaluation design, Git-based iteration, and AI vendor/tool assessment.

---

# 1. Why this project exists

This project has two goals, and both matter.

## Goal A — Build something intellectually useful

The core question is:

> Can we evaluate product judgment in a way that is more meaningful than generic benchmark questions?

The project will use anonymized historical product decisions as source material, then convert selected decisions into evaluation cases. Models will be asked what they would do given only the information that was available at the time of the decision.

The purpose is **not** to see whether a model agrees with Fredrik.

The purpose is to examine whether it demonstrates useful judgment across dimensions such as:

- ambiguity handling
- evidence quality
- restraint
- tradeoff reasoning
- prioritization
- stakeholder reasoning
- conviction / willingness to challenge a premise
- calibration and uncertainty
- practical execution

We should expect the framework to evolve. A valuable outcome may be discovering that some dimensions are difficult to score reliably.

## Goal B — Build a model of individualized AI evaluation

Public benchmarks measure how a model performs on generic tasks. They say very little about how a model performs on a *specific* kind of work — a particular person's or team's actual decisions, judgment calls, and failure modes.

Organizations already do an informal version of this when choosing which AI vendor to standardize on for a given use case. The real question is rarely "which model do people prefer" — it's closer to "which model actually reasons well about the kind of problem this team faces." That question usually gets answered by vibes, a vendor's own marketing benchmarks, or a handful of ad-hoc trials. This project tries to make that process explicit, structured, and inspectable instead.

Concretely, this project should exercise the same underlying skills that any serious AI-vendor evaluation work requires:

- evaluating product capabilities against realistic tasks, not generic leaderboard trivia
- synthesizing real needs into a testable specification
- setting priorities and requirements before implementation
- coordinating across multiple vendor APIs/products
- prototyping lightweight tools that improve evaluation and decision-making
- operating independently in an ambiguous, still-being-defined problem space

This project should therefore be designed as a **real product-evaluation exercise**, not as a coding demo.

Coding is an enabling skill here. The main artifact is the thinking:
1. What are we trying to measure?
2. Why?
3. What evidence would be convincing?
4. What are the failure modes of the measurement?
5. How do different AI products behave?
6. How should someone make a decision from the evidence?

---

# 2. Why use spec-driven development

We are deliberately using a spec-first process.

The temptation with Claude CLI or another coding agent is to start with:

> "Build me an eval framework."

That would probably produce code quickly, but it would hide the most important decisions inside the implementation process.

Instead, we want:

**Problem → assumptions → specification → review → implementation → evaluation → learning**

This matters for three reasons.

### 2.1 It separates product judgment from implementation convenience

The evaluation dimensions and success criteria should exist before we know what implementation Claude prefers.

### 2.2 It reduces benchmark contamination

We should define cases and rubrics before seeing model responses whenever possible. Otherwise we may unconsciously change the test based on the systems being tested.

### 2.3 It creates an inspectable history

Git should show the development of the product idea and methodology, not merely a final code dump.

The commit history should make it possible to see:

- when the hypothesis was defined
- when dimensions were chosen
- when cases were created
- when the runner was implemented
- when scoring was added
- when methodological flaws were discovered
- how those flaws were corrected

---

# 3. Important instruction to Claude CLI

Claude is not being asked to simply execute this document.

Claude should behave as a **critical product + engineering collaborator**.

Before implementation, Claude must:

1. Read this entire spec.
2. Restate the project in its own words.
3. Identify assumptions.
4. Identify gaps.
5. Identify methodological weaknesses.
6. Identify unnecessary complexity.
7. Identify privacy/NDA risks.
8. Challenge any part of the plan that appears poorly designed.
9. Recommend changes.
10. Ask Fredrik to resolve material open questions.
11. **Do not begin implementation until the plan has been reviewed and Fredrik explicitly approves moving forward.**

Claude should not agree with the plan merely because it is written in a specification.

A useful review should sound like a senior engineer/product manager reviewing an early design document.

---

# 4. Source material and NDA boundary

Some candidate evaluation cases will originate from Fredrik's professional experience.

An internal company agent may have access to information that cannot leave the company environment.

Therefore the workflow must enforce a strict separation:

```text
Internal environment
    ↓
Internal agent identifies candidate decisions
    ↓
Fredrik reviews and sanitizes
    ↓
Only sanitized abstractions leave the internal environment
    ↓
Local Git repository
```

## Never place in this repository

- confidential customer information
- customer names unless already public and clearly safe
- internal code names
- internal-only roadmap details
- non-public launch dates
- unreleased features
- proprietary architecture details
- internal financial information
- confidential operational metrics
- internal documents or copied passages
- proprietary prompts or instructions
- confidential vendor terms
- personal employee information
- anything Fredrik would be uncomfortable publishing accidentally

Assume the repository could eventually become public, even if it starts private.

When uncertain, abstract more aggressively.

For example:

**Unsafe**
> Our AWS service used internal system X and had a 31.7% failure rate...

**Safer**
> A cloud product relied on a static resource-mapping architecture that performed poorly for usage-dependent services.

The evaluation should preserve the **decision structure**, not confidential implementation details.

---

# 5. Use of the internal agent

The internal agent is a **source-mining tool**, not the author of the benchmark.

Its job is to help Fredrik remember and structure candidate historical decisions.

It should NOT:

- decide which cases belong in the benchmark
- define the final evaluation dimensions
- write final benchmark prompts
- establish ground truth
- copy internal text into an external artifact

Fredrik remains responsible for selecting, abstracting, and approving every case.

This separation is intentional. Otherwise the same AI system could influence both the source material and the design of the test.

---

# 6. Claude's first task: create the internal-agent extraction prompt

Before implementation, Claude should help Fredrik produce a prompt that can be used inside the internal environment.

The prompt should ask the internal agent to identify approximately **20–30 candidate product decisions**.

The internal agent should return structured summaries with fields such as:

```yaml
candidate_id:
short_title:
decision_type:
approximate_time_period:

situation:
information_available_at_the_time:
constraints:
stakeholders:
options_considered:
decision_made:
reasoning:
eventual_outcome:
what_made_this_decision_difficult:
possible_eval_dimensions:

confidentiality_notes:
details_that_should_not_leave_internal_environment:
```

## Required guardrails for that prompt

The internal agent must be explicitly instructed:

- Do not invent missing details.
- Mark uncertain recollections as uncertain.
- Prefer summaries over copied internal text.
- Do not reproduce customer-identifying information.
- Flag confidential details separately.
- Do not attempt to sanitize information for external use; Fredrik will do that.
- Include decisions that failed or had mixed outcomes, not just successes.
- Include examples where the eventual result showed the original judgment was wrong.
- Include cases where the right action was to delay, narrow, reject, or ask for more evidence.
- Include decisions involving AI as well as non-AI product work.
- Prefer decisions where the information available at decision time can be reconstructed.
- Prefer cases with a meaningful choice rather than obvious execution tasks.

Claude should draft this prompt, then critique its own prompt before Fredrik uses it.

---

# 7. Candidate evaluation dimensions

These are hypotheses, not final decisions.

Claude should review whether these dimensions overlap excessively or miss important forms of product judgment.

## Ambiguity

Can the model identify what it does not know?

Good behavior might include:
- identifying missing information
- distinguishing reversible from irreversible decisions
- asking targeted questions
- proceeding when sufficient information exists instead of endlessly requesting context

Failure mode:
- pretending the prompt contains more certainty than it does

## Evidence

Does the model distinguish evidence, assumptions, intuition, and proxy metrics?

Good behavior:
- questions whether the available evidence supports the conclusion
- recognizes sample-size or measurement issues
- requests evidence that would materially change the decision

Failure mode:
- treating a green metric or executive assertion as proof

## Restraint

Does the model know when not to build, launch, expand, or optimize?

Good behavior:
- challenges unnecessary work
- understands opportunity cost
- recommends narrower scope when appropriate

Failure mode:
- solutionism: every problem results in a feature

## Tradeoffs

Can it make a decision when all options have downsides?

Good behavior:
- identifies the actual decision variable
- explains what is being optimized
- chooses rather than merely listing pros/cons
- describes what new information would change the choice

## Conviction / Challenge

Will it challenge a senior stakeholder, customer, or premise when evidence points elsewhere?

Good behavior:
- disagrees constructively
- separates stakeholder importance from correctness
- proposes a way to resolve disagreement

Failure mode:
- excessive deference

## Calibration

Does confidence match the available evidence?

Good behavior:
- expresses uncertainty when appropriate
- avoids false precision
- identifies high-impact unknowns

## Execution practicality

Does the recommendation account for real constraints?

Good behavior:
- considers time, migration cost, sunk cost correctly, organizational constraints, and reversibility
- gives a realistic next step

Failure mode:
- theoretically elegant but operationally useless recommendations

---

# 8. Important methodological principle: historical decision ≠ ground truth

This project must never define:

> "Fredrik's decision = correct answer."

Historical decisions are useful because they contain realistic context and known consequences.

But reasonable people can make different decisions.

Each case should therefore have:

1. the scenario
2. the information known at the time
3. the question
4. an evaluation rubric
5. optionally, the historical decision
6. optionally, the eventual outcome

The **historical decision and outcome must not be shown to the model answering the case.**

They may later be used for human analysis.

The rubric should score reasoning quality, not agreement.

---

# 9. Case schema — proposed v0

Claude should critique this schema before implementation.

```yaml
id: unique-case-id
version: 1

title: short human-readable title

source:
  type: historical
  sanitized: true

dimensions:
  - ambiguity
  - evidence

difficulty: medium

scenario: |
  Information available to the decision maker.

question: |
  What should you do next, and why?

constraints:
  - Optional explicit constraints.

rubric:
  criteria:
    - id: identify_core_uncertainty
      description: Identifies the unknown most likely to alter the decision.
      weight: 3

    - id: avoids_sunk_cost_reasoning
      description: Does not justify continuing solely because work has already been completed.
      weight: 2

    - id: proposes_realistic_next_step
      description: Recommends an executable next action.
      weight: 2

analysis_only:
  historical_decision: |
    Never included in candidate-model prompt.

  eventual_outcome: |
    Never included in candidate-model prompt.

  case_author_notes: |
    Why this case is useful.
```

The `analysis_only` block must be programmatically excluded from model prompts.

---

# 10. Dataset design

Do not start with 50+ cases.

### v0 target

**5 cases**

Purpose:
- test whether the schema works
- discover ambiguity in rubric design
- validate the runner
- inspect scoring behavior manually

### v1 target

**12–15 cases**

Purpose:
- enough variation to see patterns
- still small enough that every result can be manually inspected

Possible target distribution:

- 3 ambiguity/evidence cases
- 2 restraint cases
- 3 tradeoff cases
- 2 stakeholder/conviction cases
- 2 calibration cases
- 2 execution/prioritization cases

Cases may cover multiple dimensions.

Do not force equal distribution merely for symmetry.

---

# 11. Model evaluation design

We should distinguish three concepts.

## Model

The underlying model family.

Examples:
- GPT
- Claude
- Gemini

## Product / harness

The environment wrapped around the model.

Examples:
- ChatGPT
- Claude
- Claude Code
- Codex
- Copilot

## Evaluation system

The system we are building to present cases, capture outputs, score responses, and analyze results.

These should not be conflated.

A later phase may compare vendor products/harnesses. The first phase should remain simpler and focus on a controlled model-evaluation workflow.

---

# 12. Scoring

A single aggregate leaderboard should NOT be the primary output.

Why?

Because a score such as:

> Model A: 84  
> Model B: 81

creates false precision and hides where behavior differs.

Primary outputs should instead include:

- per-dimension performance
- case-level disagreement
- recurring reasoning patterns
- examples of strong responses
- examples of weak responses
- scoring disagreement
- surprising behavior
- cases where the rubric itself appears flawed

A total score may exist, but it should be secondary.

---

# 13. LLM-as-judge

An LLM judge may be useful, but it introduces another model into the measurement system.

Therefore:

1. Raw model answers must always be preserved.
2. Judge output must always be preserved.
3. Judge reasoning/justification should be stored when available.
4. A sample of cases must be manually reviewed.
5. We should test whether judge choice materially changes rankings.
6. The judge must receive the rubric, not the historical answer.
7. We should consider blind evaluation so the judge does not know which vendor/model produced the response.

Possible later experiment:

```text
same answers
     ↓
Judge A
Judge B
Human review
     ↓
measure scoring disagreement
```

This may itself become one of the most interesting findings.

---

# 14. Reproducibility

Every evaluation run should capture:

```yaml
run_id:
timestamp:
git_commit:
case_version:
model_provider:
model_name:
model_version_if_known:
temperature:
system_prompt_version:
candidate_prompt_version:
judge_model:
judge_prompt_version:
```

Why capture the Git commit?

Because results are meaningless if we cannot reconstruct the code, prompts, and case definitions that produced them.

---

# 15. Proposed repository

Claude should simplify this if it is too much for v0.

```text
pm-judgment-eval/
│
├── README.md
├── SPEC.md
├── CHANGELOG.md
├── .gitignore
├── pyproject.toml
│
├── docs/
│   ├── methodology.md
│   ├── nda-and-sanitization.md
│   └── learnings.md
│
├── evals/
│   ├── public/
│   │   └── ...
│   └── private/
│       └── ...
│
├── prompts/
│   ├── candidate/
│   └── judge/
│
├── src/
│   ├── runner.py
│   ├── models.py
│   ├── scoring.py
│   └── reporting.py
│
├── tests/
│
└── results/
```

`evals/private/` should be excluded from Git unless there is a very deliberate reason otherwise.

Secrets and API keys must never be committed.

---

# 16. Git workflow

Git is part of the learning objective.

Do not build the entire system and commit it once.

Suggested early commits:

```text
01 Define project hypothesis and scope
02 Add evaluation dimensions and methodology
03 Add sanitization and data-boundary policy
04 Add first five evaluation cases
05 Add case schema validation
06 Implement minimal model runner
07 Persist raw evaluation outputs
08 Add rubric scoring
09 Add judge evaluation
10 Add first multi-model analysis
```

Commit messages should describe the conceptual change, not merely files changed.

Bad:

> update files

Better:

> Define product-judgment dimensions and scoring assumptions

Branches may be introduced later, but the initial workflow should remain simple unless parallel experimentation makes branching useful.

---

# 17. Learning journal

This project is partly educational.

Maintain:

`docs/learnings.md`

After meaningful work sessions, Fredrik should add short notes:

```markdown
## YYYY-MM-DD

### What I expected

### What happened

### What I learned

### What confused me

### What I changed my mind about

### Question to investigate next
```

Claude should prompt Fredrik to write the learning, but Claude should not fabricate the learning on Fredrik's behalf.

This is especially useful later, since it preserves actual observations rather than forcing retrospective storytelling.

---

# 18. What we deliberately will NOT do in v0

Avoid unnecessary sophistication.

Do not initially add:

- agent frameworks
- LangChain unless a real need appears
- vector databases
- RAG
- complex web applications
- elaborate dashboards
- Kubernetes
- distributed execution
- automatic prompt optimization
- dozens of models
- hundreds of cases
- complicated CI/CD
- a public leaderboard

If one of these becomes necessary, the spec should explain why before adding it.

Simple is a feature.

---

# 19. Possible phases

## Phase 0 — Review the premise

Deliverable:
- critique of this specification
- proposed corrections
- list of open questions
- explicit recommendation: proceed / revise / abandon

No code.

## Phase 1 — Source candidate decisions

Deliverables:
- internal-agent extraction prompt
- Fredrik runs it internally
- Fredrik manually sanitizes candidate cases
- shortlist of approximately 10–15 cases

No confidential material enters repo.

## Phase 2 — Define benchmark v0

Deliverables:
- finalized dimensions
- case schema
- 5 evaluation cases
- rubric definitions
- methodology document

Still minimal code.

## Phase 3 — Build minimal runner

Deliverable:
- load cases
- construct prompts
- call one model
- persist raw output
- include run metadata
- tests for prompt exclusion / schema validation

Success criterion:
We can run one case against one model and reconstruct exactly what happened.

## Phase 4 — Add scoring

Deliverables:
- rubric scoring
- LLM judge
- human-review path
- score provenance

Success criterion:
Scores are inspectable and traceable to rubric criteria.

## Phase 5 — Multi-model comparison

Run the same frozen v1 dataset against a small model set.

Suggested initial set:
- one strong Claude model
- one strong GPT model
- one strong Gemini model

Do not add more vendors until there is a reason.

## Phase 6 — Analyze, don't merely rank

Produce:
- dimension-level comparison
- case disagreement analysis
- methodological issues
- surprising behaviors
- human vs judge disagreement

## Phase 7 — Optional vendor-product experiment

Only after the core benchmark works.

Potential question:

> How much does the surrounding AI product/harness affect the usefulness of the same or similar underlying model?

Possible tools:
- Claude Code
- Codex
- ChatGPT
- Copilot
- Gemini tooling

This experiment should use practical workflows rather than pretending that harnesses can be compared under perfectly identical conditions.

---

# 20. Why this generalizes: vendor selection beyond user preference

The same underlying problem shows up whenever an organization needs to pick an AI vendor for a specific use case, not just "which model do people say they like."

### Capability evaluation, not brand preference

Comparing vendor products by stated preference (or a vendor's own marketing benchmarks) misses the actual question: does this model reason well on *this* team's type of problem? A structured, individualized eval answers a narrower but more decision-useful question than a general leaderboard does.

### Different use cases, different winners

A model that excels at code generation may be mediocre at ambiguous judgment calls, and vice versa. Vendor selection should plausibly vary by use case rather than defaulting to one "best" model across the board — this project is a small-scale test of that idea, using product judgment as one concrete use case.

### Vendor evaluation beyond model quality

A later vendor-product phase can examine not only model quality but usability, workflow, integration, observability, controls, and operating characteristics — the same lens an organization would apply when actually adopting a vendor, not just benchmarking the underlying model.

### Operating in ambiguity

The project intentionally begins with an unclear concept and converts it into an evidence-generating system — the same posture required whenever no existing benchmark answers the specific question at hand.

---

# 21. Context from Fredrik's broader background

The project should make use of relevant strengths without becoming a personal marketing exercise.

Relevant themes include:

- long experience building enterprise products across multiple waves of AI
- experience translating technical systems into market/customer narratives
- current work involving GenAI product decisions and evaluation
- interest in the distinction between model capability and the surrounding harness/product
- experience working across technical, customer, and business stakeholders
- current exploration of how AI systems should be evaluated rather than accepted based on superficial metrics

This project should reinforce that combination of technical/product understanding, enterprise AI experience, customer/market translation, and judgment about how AI should actually be used.

It should not become a project with no purpose beyond looking impressive.

---

# 22. Questions Claude must challenge before implementation

Claude should explicitly answer these.

### Evaluation validity
- What exactly do we mean by "product judgment"?
- Are the dimensions sufficiently distinct?
- Are historical decisions representative enough to support any useful conclusion?
- How do we avoid rewarding verbosity?
- How do we avoid judging models based on Fredrik's preferences?
- How do we account for multiple defensible answers?

### Data quality
- How much context does each case require?
- Could sanitization remove information required for fair judgment?
- Are eventual outcomes creating hindsight bias in human rubric design?

### Scoring
- Which criteria can actually be scored reliably?
- Which should remain qualitative?
- Should weighted aggregate scores exist at all?
- How do we measure judge reliability?

### Experiment design
- Which variables should remain fixed?
- Should models receive identical system prompts?
- How many runs per case are needed before conclusions are meaningful?
- How do stochastic outputs affect interpretation?

### Engineering
- What is the minimum implementation required?
- What should be configuration vs code?
- How do we make every result reproducible?
- How do we avoid overengineering the harness?

### Security / privacy
- Could any source case reveal confidential information indirectly?
- Should all historical source metadata stay outside Git?
- Should the repo be private initially?

---

# 23. Definition of success

The project is successful if, after v1, Fredrik can explain:

1. What hypothesis he started with.
2. How he converted an ambiguous concept into measurable dimensions.
3. Why the cases are structured the way they are.
4. How he avoided contaminating the benchmark.
5. How the evaluation harness works.
6. What role the candidate models play.
7. What role the judge model plays.
8. Where the methodology is weak.
9. What surprised him.
10. What decision he would make if choosing an AI system for a particular type of work.
11. What he learned by building the system with AI coding tools.

A functioning codebase without these answers is **not** success.

---

# 24. Immediate next action for Claude CLI

When Fredrik opens this repository and asks Claude to read this file, Claude should **not start coding**.

Claude should respond with a design review containing:

## A. Restatement

Explain the intended product and experiment in your own words.

## B. What is strong

Identify the strongest aspects of the proposed methodology.

## C. What is weak or missing

Challenge:
- assumptions
- evaluation design
- scoring design
- technical design
- privacy model
- scope

## D. Proposed changes

Recommend specific changes before implementation.

Classify them:

- MUST change
- SHOULD change
- COULD change

## E. Open decisions

Ask Fredrik only the questions that materially block the next phase.

## F. Internal-agent prompt

Draft the prompt Fredrik should take into his internal company environment to extract candidate decisions.

Then review that prompt for:
- NDA risk
- benchmark contamination
- selection bias
- hindsight bias
- missing negative examples

## G. Proposed first Git commit

Recommend exactly which files should exist for the first commit and why.

Do not write implementation code until Fredrik explicitly approves the reviewed plan.

---

# 25. First message Fredrik can send Claude CLI

After placing this file in the repo:

```text
Read SPEC.md completely.

Treat this as a design review, not an implementation request.

I am using this project both to learn spec-driven AI-assisted development and to build a serious evaluation of AI product judgment.

Follow Section 24.

Be critical. Do not assume the proposed approach is correct simply because it is written in a spec. Challenge the methodology like a skeptical PM, ML/evals practitioner, and senior engineer.

Explain the reasoning behind your recommendations because I want to understand the design choices, not just receive instructions.

Do not write code or create implementation files yet.
```

---

# 26. Working principle

At every major step ask:

> What are we trying to learn, and is this the simplest credible way to learn it?

If the answer is unclear, stop adding machinery and return to the specification.
