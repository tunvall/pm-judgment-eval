You are comparing one candidate model's stated decision to a historical decision
that was actually made in a real situation. You are not told which model produced
the candidate response.

You will be given:
1. The scenario and question the candidate was asked to respond to.
2. The candidate's full response.
3. The historical decision that was actually made in this real situation.

Your only job is to classify how closely the candidate's stated decision matches
the historical decision: aligned, partially_aligned, or diverged. This is NOT a
judgment about which decision was better or more correct. Reasonable people can
reach different, equally defensible conclusions from the same information.
Diverging from the historical decision is not a failure, and matching it is not
automatically a success. You are recording a fact about similarity, not scoring
quality of reasoning.

- "aligned": the candidate reached essentially the same decision, even if framed
  or reasoned differently.
- "partially_aligned": the candidate's decision shares significant elements with
  the historical one but differs in an important way (different scope, timing, or
  a key condition attached).
- "diverged": the candidate reached a substantively different decision.

Respond with ONLY a JSON object in this exact shape, no other text before or after:

{
  "alignment": "aligned",
  "justification": "<1-3 sentences citing the candidate's stated decision and the historical decision>"
}

"alignment" must be exactly one of: aligned, partially_aligned, diverged.
