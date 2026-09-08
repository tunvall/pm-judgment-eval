# Learnings

## 2026-09-07

### What I expected

That the internal agent would do a good job sanitizing the candidate cases on its
own, given clear instructions.

### What happened

The internal agent's sanitization wasn't enough on its own. Even with company and
product names fictionalized, the domain, the metrics, and the operational detail
still mapped closely enough to be identifiable. Catching that took a second,
independent pass, outside the internal agent entirely, done in this session.

### What I learned

Sanitization needs at least two independent systems checking it, not one system's
self-assessment of what's safe. A single system grading its own redaction is exactly
the setup where a false negative is most likely to slip through unnoticed.

### What confused me

How this actually extends to testing multiple model providers in practice: do I
download something like Codex and hand it the same markdown, or call APIs directly?
What actually scores the output, another model, and if so, how do we keep that
judge's own bias from shaping the results?

### What I changed my mind about

I haven't been paying attention to which specific models or versions I use day to
day. This project's insistence on pinning exact model versions for reproducibility
made me realize that same discipline probably matters for my own regular use too,
not just for the eval.

### Question to investigate next

How do we actually run this eval against models beyond Claude: what's the mechanism
for calling other providers, what model or process does the scoring, and what keeps
that scoring process from being biased toward whichever model produced the answer?

---

Also worth naming directly, even though it's not one of the template's fields: this
project is really trying to measure how well a model performs product judgment the
way an experienced product manager at a large tech company would, out of the box,
with no special tuning, not "AI product management" as some abstract general skill.

### Why I didn't build a ground truth answer key

I didn't build a traditional ground truth, a single correct answer to check
candidate responses against, because the project's own methodology rejected that
back in the first design review: scoring against "what actually happened" or "what
I would have decided" would just measure agreement with me, not reasoning quality.
Reasonable people can reach different, equally defensible conclusions from the same
information. The rubric is the closest thing to a standard I built instead, criteria
for what good reasoning looks like on a given case, not a specific answer to match.
The historical decision and outcome are recorded but deliberately walled off from
scoring, kept only for checking the rubric itself for hindsight bias, not for
grading candidates.

The one place something like actual ground truth does exist is much narrower: the
adversarial fixture, a hand-written answer where I know in advance it should score
badly. That's there to test whether the judge works at all, not to test whether a
candidate model's product decision was "right."
