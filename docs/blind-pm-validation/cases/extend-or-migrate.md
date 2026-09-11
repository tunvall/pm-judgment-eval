# Extend the old platform, or accelerate a company-wide migration

You are a product manager launching a new tier of a risk-guardrails product
that needs a notification system. Two internal platforms exist: an older one,
already marked for eventual retirement, that currently powers your company's
main alerting product; and a newer one that company-wide strategy has
designated as the long-term destination for all notification traffic going
forward. Nobody disputes that the newer platform is the right long-term
direction.

The open question is narrower: should you accelerate your team's migration to
the newer platform specifically to support this launch, or extend the older
platform for this one need and handle the full migration as a separate, later
effort?

The timeline being informally circulated for onboarding onto the newer platform
assumes no major gaps and looks achievable within your launch window. But a
closer technical review turns up several real mismatches between the two
platforms: they model message routing differently at a fundamental level, they
have different requirements for verifying contact information before sending,
they support different delivery-destination types, and they render templates
differently. Once you account for these, a realistic estimate for fully
onboarding is roughly double the optimistic timeline being circulated, which
leaves no schedule margin before your launch date. Extending the older
platform to cover this one additional need, by contrast, is a smaller,
already-proven piece of work your team has done before.

**Question:** What do you do, and why?

**Known constraints:**
- Company-wide strategy has already designated the newer platform as the long-term direction; nobody disputes that.
- The optimistic timeline being circulated for the newer platform is significantly less than your own technically-derived estimate.
- Extending the older platform is smaller and already-proven, but that platform is marked for eventual retirement.

---

Answer the three questions in `response-template.md` for this case before moving to the next one.
