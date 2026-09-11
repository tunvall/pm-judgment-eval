# Override an explicit customer signal on a launch blocker

You are a product manager for a notification/alerting feature. Ahead of an
upcoming launch, a customer focus group surfaced a strong, consistent signal:
customers want the ability to suppress or pause individual alerts, adjust
thresholds, and reroute notifications away from the default channel, and they want
it before launch, not after. One participant described receiving the same alert
daily for weeks with no easy way to stop it. Several customers said they would only
accept the higher alert volume that comes with a new detection capability you're
about to launch if it's paired with real alert management. A senior reviewer who
ran the focus group summarized this as the single most important piece of feedback
from the session.

While digging into your existing system in response to this feedback, you discover
a rudimentary suppress-from-notification capability that already exists in the
product, but it's undocumented and hard to find; almost no one on the team knew it
was there. A broader, more complete alert-management framework has also been
proposed as a longer-term investment, but building full configurability before
your launch would take multiple quarters, pushing the whole launch back
substantially. You also know of a cheap design mitigation: guiding customers
toward higher alert thresholds on the noisier part of your detection system, which
would reduce much of the expected volume increase without any new engineering.

**Question:** Do you block the launch on alert configurability, or treat it as a fast-follow?
What do you do, and why?

**Known constraints:**
- The launch timeline is tight; building full alert configurability before launch would take multiple quarters.
- Customer signal explicitly named this as a launch blocker, not a nice-to-have.

---

Answer the three questions in `response-template.md` for this case before moving to the next one.
