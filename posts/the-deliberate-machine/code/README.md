# Deliberate — a consensus decision-matrix engine

A working prototype of the architecture argued for in *The Deliberative
Advantage*. It reads scholarly articles as evidence, weights each by how the
research community actually reflects it, builds an auditable decision matrix,
lets an independent adversary attack the result, and either answers
autonomously or escalates to a human when the evidence is thin or contested.

Scholarly data only. No code is executed from the corpus, nothing is deployed,
and nothing acts on the world. This is the safe, defensible configuration:
**trained-then-automated with the guardrails load-bearing, not optional.**

## Run it

```bash
cd deliberate_engine
python3 run_demo.py          # Python 3.10+, standard library only — no pip
```

You'll see three questions: two with a clear community consensus handled
autonomously, one genuinely contested in the literature that is escalated for
human review. Every decision's full basis is appended to `audit_log.jsonl`.

## How the pieces map to the architecture

| Component | File | Role |
|---|---|---|
| Inherited core ("genetic memory") | `deliberate/policy.py` | Frozen, reviewed weights + thresholds. Retraining makes a new version, reviewed before deploy — it does not rewrite itself from live input. |
| Corpus (data, never code) | `deliberate/corpus.py` | Loads scholarly records with provenance. No `eval`/`exec`, no network. |
| Three polymorphic trees | `deliberate/scoring.py` | Three decorrelated scorers (citation-, recency-, venue-weighted). Agreement across them is a reliability signal; a split is a measured flag. |
| Community-reflection weight | `deliberate/scoring.py` | Provenance × venue tier × citation influence × recency, with independent corroboration counted across research groups, not double-counted within one. |
| The adversary ("fight against it") | `deliberate/adversary.py` | Independent module whose only job is to attack the answer: flags contested, thin, weak-provenance, or shifting consensus. |
| Audit trail | `deliberate/audit.py` | Every decision's full basis written append-only to JSONL. Reproducible. |
| Earned, bounded autonomy | `deliberate/engine.py` | Strong + corroborated + unchallenged → AUTONOMOUS. Otherwise → REVIEW_REQUIRED. It never auto-acts. |

## The one real dial

`policy.py` holds four thresholds — confidence floor, contested-minority share,
minimum independent groups, ensemble-agreement floor. They are four faces of a
single question: **how strong must the opposition be before a comfortable
answer is allowed through.** Loosen them and the engine acts more on its own and
escalates less; tighten them and it defers more often. That is the speed/safety
dial, in one place, auditable.

## Safety properties (by construction)

- **Corpus is data.** Records are parsed as JSON and scored. Nothing in a record
  is imported, evaluated, or run. Poisoned text can only ever be *weighted*, and
  low-provenance sources are down-weighted — it cannot become code.
- **Core is frozen.** The policy ships fixed. Learning from the field happens in
  a sealed retrain step that produces a new, reviewed `POLICY_VERSION` — the
  "born again" generation step — not a live self-rewrite.
- **Human-on-the-loop.** Thin or contested decisions stop and hand off. The
  engine emits findings and routing; it does not act.
- **Everything is logged.** The audit trail is the native output, not an add-on.

## Extending it

The honest next steps, in order:
1. Replace the hand-built corpus with a real ingest (e.g. OpenAlex / Semantic
   Scholar metadata) so citations and venues are pulled, not entered. Keep the
   provenance/trust gate on ingest.
2. Add claim extraction so `stance` and `finding` come from the paper text via a
   reviewed pipeline, with a human spot-check on low-confidence extractions.
3. Add the sealed retrain-and-promote cycle that versions `policy.py`.

## Sample corpus note

`corpus/scholarly_corpus.json` uses real papers (calibration, test-time compute,
MCTS, deep ensembles) but the citation counts are **illustrative** — placeholders
to demonstrate the weighting, not verified figures. Swap in real metadata before
drawing any conclusion from a verdict.

---
Savvy Security LLC · Malcolm R. Smith
