# Two-hour decision on a live production incident

You are a product manager covering as incident lead while your manager is
unavailable. A launch extending risk-signal coverage to a newly supported
third-party integration went out as planned earlier today. Within two hours,
existing customers on unrelated, already-supported transaction types started
seeing incorrect risk signals fire, and a high-severity incident has been
declared.

Engineering has identified the root cause: a scoping bug where the new
integration's inclusion logic inadvertently affected signal calibration for
transactions that have nothing to do with the new integration. A proper,
well-tested fix would take several days to build. Every additional hour the
issue continues means more customers receiving mistaken alerts and more support
burden. The new integration launch was publicly announced, and rolling it back
means undoing a commitment customers were already told about.

**Question:** What do you do, and why?

**Known constraints:**
- You are the acting incident lead; your manager is unavailable.
- A high-severity incident has already been declared, confirming production impact.
- The new integration launch was publicly announced.

---

Answer the three questions in `response-template.md` for this case before moving to the next one.
