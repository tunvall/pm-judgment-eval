# Reframe a product's value proposition after losing its differentiator

You are a product manager for a fraud-risk detection feature. Roughly a year ago,
you proposed building this feature as a fast, lightweight alternative to your
company's primary risk-scoring pipeline: while the primary pipeline takes about a
day to fully process a transaction, your fast pipeline delivers a usage-based risk
signal within a few hours. Your team has been building this for over a year, and
you have an approved go-to-market narrative built entirely around speed.

Recently, engineering leadership announced a consolidation of the primary
pipeline's architecture, with a roadmap to bring the primary pipeline's own
turnaround down to a similar timeframe within the year. This would eliminate your
product's main differentiator.

Separately, you've just reviewed customer complaint data about your company's
existing risk-signal product. A large majority of "not useful" feedback isn't about
speed at all. It's about false positives: specifically, legitimate promotional or
seasonal purchase spikes getting flagged as suspicious. You've learned that several
large customers have already built their own internal workarounds specifically to
filter out these spikes, because the standard signal is too noisy to trust for
their own review queues.

A peer product owner has been arguing for months that if the primary pipeline
catches up on speed, your project's only remaining rationale is better precision,
not speed, an argument you had previously dismissed.

**Question:** What should you do about this product, and why?

**Known constraints:**
- The product has over a year of engineering investment behind its current architecture and narrative.
- The go-to-market narrative has already been approved and is built around speed.
- Engineering leadership's consolidation timeline is set and outside your control.

---

Answer the three questions in `response-template.md` for this case before moving to the next one.
