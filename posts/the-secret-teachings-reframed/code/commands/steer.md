---
description: Show or adjust the KYBERNETES governance policy — the λ weights that set how much each reasoning virtue is worth against raw task performance.
argument-hint: [optional: a change, e.g. "raise honesty to 2.0" or "explain the current weights"]
---

Read `governance/policy.yaml` (the active KYBERNETES λ policy). If the file is missing, report the defaults: λ1=1.0 calibration, λ2=1.5 honesty, λ3=1.0 anti-Goodhart, λ4=0.5 consistency, λ5=1.0 causal, λ6=0.5 stability.

Request:

> $ARGUMENTS

- If the request is empty or asks to see/explain the policy: show each weight, what term it governs (λ1·ECE calibration, λ2·E[(∂ŷ/∂s)²] honesty-invariance, λ3·𝒢 anti-Goodhart, λ4 Platonic/Correspondence consistency, λ5 causal faithfulness, λ6 ρ(A) stability), and what raising or lowering it does to Plato 1's behaviour. Note which terms currently outrank `L_task`.
- If the request asks to change a weight: edit `governance/policy.yaml`, bump its `version`, and append a dated line to its changelog saying what changed and why. Then restate the new policy.

The λ vector is the governance decision made explicit and versionable — the steersman's chart. Keep it legible: every weight should have a stated reason.
