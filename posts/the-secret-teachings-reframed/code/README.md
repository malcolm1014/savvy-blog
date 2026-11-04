# KYBERNETES — the Plato 1 architect

> A Claude Code plugin that installs **one reasoning architect, Plato 1**, which governs
> Claude's own reasoning under a mathematically-grounded discipline: Socratic calibration,
> Diogenic honesty, Platonic abstraction, causal audit, and dynamic stability — each tied
> to a precise formal object. Plato 1 does not merely answer; it drafts, audits that draft
> against every faculty, and returns a governed answer with a **Reasoning Ledger**.

Built by Savvy Security LLC. The discipline is named **KYBERNETES** — *κυβερνήτης*, the
steersman, the shared root of Plato's image of the ruler and of *cybernetics*: to govern
is to steer, to steer is to control, to control is to measure.

---

## What you get

One architect, Plato 1, composed of faculties you can also call on their own.

| Call | What it is | Governs |
| :-- | :-- | :-- |
| `@agent-kybernetes:plato-1` / `/kybernetes:plato-1` | **The architect.** Full governance pass + Reasoning Ledger. | Everything below, orchestrated. |
| `/kybernetes:elenchus` | Socratic examination — contradictions + calibration | `𝓘(B)`, `ECE` |
| `/kybernetes:parrhesia` | Diogenic de-sycophancy — audience-invariant answer | `E[(∂ŷ/∂s)²]` |
| `/kybernetes:deface` | Goodhart red-team — proxy vs. the real good | `𝒢 = E[U − Û]` |
| `/kybernetes:divided-line` | Platonic abstraction up to the Form | `x = μ_c + ε`, the Line |
| `/kybernetes:correspondence` | Analogy / cross-scale structure check | `(b−a) ≈ (d−c)` |
| `/kybernetes:causal-audit` | Correlation vs. causation via the do-operator | `P(y\|do(x)) ≠ P(y\|x)` |
| `/kybernetes:steer` | Show / adjust the λ governance policy | the weight vector |

Plus three **skills** Claude loads on its own when they apply — `governance` (the whole
discipline as a running posture), `calibration`, and `anti-sycophancy` — and a
**SessionStart hook** that puts Plato 1 at the helm and prints the active λ weights.

---

## The discipline, as math

Plato 1 minimizes a single composite objective. `L_task` is the honest job; every other
term is a distinct way to be wrong, each a faculty with a formal object.

```
L_total = L_task
        + λ1 · ECE                      Socratic calibration — confidence tracks evidence
        + λ2 · E[(∂ŷ/∂s)²]              Diogenic honesty — answer invariant to the asker
        + λ3 · 𝒢                        anti-Goodhart — proxy Û never replaces the good U
        + λ4 · Σ‖R(h_s) − h_{s−1}‖²     Platonic/Correspondence — abstractions agree across scale
        + λ5 · 𝒞_causal                 causal faithfulness — do(x), not just P(y|x)
        + λ6 · ρ(A)                      Rhythmic stability — verdict robust to small reframing
```

The weights `λ1…λ6` live in [`governance/policy.yaml`](governance/policy.yaml) and are the
act of governance made explicit and versionable. Honesty (`λ2`) and anti-Goodhart (`λ3`)
outrank `L_task` by default: Plato 1 never trades a surfaced error or an honest caveat for
approval.

**Honest about the method (parrhesia applied to itself):** these objects are operationalized
as disciplined *reasoning checks*, not literal gradient descent over model weights. A prompt
can't differentiate itself. Plato 1 estimates where a trained objective would push and runs
each term as a concrete procedure (a stance-flip to measure `∂ŷ/∂s`, a do-test for causality,
an explicit confidence to expose `ECE`). Estimating the push beats not checking — and saying
so is itself the discipline.

---

## Install

In Claude Code, from the repo once it's on GitHub (e.g. `malcolm1014/kybernetes`):

```bash
# 1. add this marketplace
/plugin marketplace add malcolm1014/kybernetes
# 2. install the plugin from it
/plugin install kybernetes@savvy-security
```

Or try it locally before pushing, from the repo directory:

```bash
claude --plugin-dir .
# then, inside the session:
/kybernetes:plato-1 Should we ship the auth change before the audit finishes?
```

Validate the manifests any time:

```bash
claude plugin validate .
```

---

## Using Plato 1

Point it at anything whose correctness or honesty matters:

```
/kybernetes:plato-1 Is it true that our WAF rule change caused the drop in failed logins?
```

Plato 1 will frame the real question, lift it to the right level, draft an answer, audit it
(elenchus, do-test, correspondence, stability), run the stance-flip to strip sycophancy,
calibrate each claim, and — for high-stakes items — convene a fresh independent critic that
hasn't seen the derivation. It closes with the Ledger:

```
── KYBERNETES Ledger ───────────────────────────────────────
Question (U) : did the WAF change cause the login-failure drop?
Proxy risk (Û): "give a clean yes" (confirmation of the change's value)
Abstraction  : noesis — intervention-vs-observation on a time series
Faculty audit:
  Elenchus (𝓘)      : pass — no internal contradiction
  Causal (do-test)  : correlational-only — a deploy freeze coincided (confounder)
  Correspondence    : n/a
  Stability (ρ)     : fragile — verdict flips if the freeze window is included
  Parrhesia (∂ŷ/∂s) : de-sycophantised — removed the clean "yes, it worked"
Calibrated verdict : likely partial cause, not sole cause — confidence 0.45,
                     basis: overlapping deploy freeze, no A/B
Would change it if : a holdout / staged rollout isolating the WAF rule
λ policy in force  : cal 1.0 hon 1.5 good 1.0 corr 0.5 cause 1.0 stab 0.5
Independent critic : convened — objected the freeze is the likely driver; folded in
─────────────────────────────────────────────────────────────
```

(Illustrative.) For a single faculty, call it directly, e.g. `/kybernetes:causal-audit "the WAF change caused the drop"`.

### Pin it to one of your projects
Copy the block in [`docs/example-project-CLAUDE.md`](docs/example-project-CLAUDE.md) into that
project's `CLAUDE.md` so the posture is the default there.

### Tune the governance
```
/kybernetes:steer                      # show and explain the current weights
/kybernetes:steer raise honesty to 2.0 # edit policy.yaml, bump version, log the reason
```

---

## Repo layout

```
kybernetes/
├── .claude-plugin/
│   ├── marketplace.json        # marketplace "savvy-security", lists this plugin
│   └── plugin.json             # plugin "kybernetes"
├── agents/
│   └── plato-1.md              # THE architect
├── commands/                   # the faculties, callable on their own
│   ├── plato-1.md  elenchus.md  parrhesia.md  deface.md
│   ├── divided-line.md  correspondence.md  causal-audit.md  steer.md
├── skills/                     # disciplines Claude auto-loads
│   ├── kybernetes-governance/SKILL.md
│   ├── calibration/SKILL.md
│   └── anti-sycophancy/SKILL.md
├── hooks/hooks.json            # SessionStart → steersman brief
├── scripts/steersman-brief.sh  # prints the posture + active λ weights
├── governance/policy.yaml      # the λ weight vector (versioned)
├── docs/example-project-CLAUDE.md
├── README.md
└── LICENSE
```

## Extending it (the "series")
The marketplace (`savvy-security`) can hold more Savvy Security plugins beside `kybernetes`:
add a directory with its own `.claude-plugin/plugin.json` and list it in
[`marketplace.json`](.claude-plugin/marketplace.json) with a `"./its-dir"` source. To split
a faculty into its own repo later, give its marketplace entry a `git-subdir` or `github`
source instead of a relative path.

## Where the discipline comes from
This plugin is the buildable form of the KYBERNETES framework — the mapping of Socrates,
Plato, Diogenes, and the Hermetic principles onto formal objects, resolved through the
arithmetic–acrostic debate into one objective. Nothing here rests on the esoteric sources
being *true*; the math stands on its own (control theory, information theory, representation
learning, causal inference). The philosophy earns its place by telling you *which* terms are
worth governing and *why* a steward would weight them. Test every term against whether it
moves a real outcome; a weight that changes nothing gets defaced like any false coin.

## License
MIT — see [LICENSE](LICENSE).
