---
description: Causal audit — separate correlation from causation in a claim using the do-operator, before the claim is trusted or acted on.
argument-hint: <the causal claim, e.g. "X causes / drives / leads to Y">
---

Run a **causal audit** on:

> $ARGUMENTS

Formal object: `P(y | do(x)) ≠ P(y | x)`. Observing `x` (seeing) is not intervening on `x` (doing). An association can be fully explained by a confounder `z` with `z → x` and `z → y`, by reverse causation `y → x`, or by selection.

Do this:
1. State the claimed cause `x` and effect `y`.
2. Sketch the **structural model**: the plausible nodes and arrows, including candidate confounders `z`, the possibility of reverse causation, and any selection/collider effects.
3. Apply the **do-test**: would `y` actually change if we *intervened* to set `x` — `do(x)` — holding the rest as-is? Or is the observed `P(y|x)` explained by the alternatives in step 2?
4. Assess what evidence exists: is there an actual intervention, a natural experiment, or only observation? Only intervention (or a valid identification strategy) licenses a causal claim.
5. **Verdict**: `causal` (with the mechanism and the evidence that identifies it), `correlational-only` (naming the most likely confounder or alternative), or `underdetermined` (saying what experiment would settle it).

Do not upgrade correlation to cause to make a cleaner story. If it's only an association, label it one.
