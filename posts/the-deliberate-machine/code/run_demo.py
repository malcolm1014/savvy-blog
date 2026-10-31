"""
run_demo.py — run the engine over the scholarly corpus on three questions.

    python run_demo.py

Two questions have a clear community consensus and are handled autonomously;
one is genuinely contested in the literature and is escalated for human review.
Every run appends its full basis to audit_log.jsonl.
"""

from pathlib import Path
from deliberate import load_corpus, deliberate, Decision

CORPUS = Path(__file__).parent / "corpus" / "scholarly_corpus.json"
LOG = Path(__file__).parent / "audit_log.jsonl"

QUESTIONS = [
    ("Is miscalibrated overconfidence a primary reliability risk in deployed LLMs?",
     "llm_overconfidence_risk"),
    ("Does allocating more compute at inference time improve LLM correctness?",
     "inference_time_compute"),
    ("Does forcing predictive diversity improve deep-ensemble reliability?",
     "forced_ensemble_diversity"),
]

BAR = "=" * 72


def show(d: Decision) -> None:
    print(BAR)
    print(f"Q: {d.question}")
    print(f"   policy {d.policy_version}")
    print("-" * 72)
    print(f"  VERDICT      {d.verdict}   confidence {d.confidence:.2f}")
    flag = ">>> HUMAN REVIEW" if d.routing == "REVIEW_REQUIRED" else "handled autonomously"
    print(f"  ROUTING      {d.routing}   ({flag})")
    print(f"  reason       {d.reason}")
    print()
    print("  Decorrelated scorers (the polymorphic trees):")
    for s in d.ensemble:
        print(f"    - {s.scorer:<18} {s.verdict:<10} net={s.net:+.2f} "
              f"(indep. groups: {s.independent_groups_majority})")
    print(f"    ensemble agreement: {d.ensemble_agreement:.0%}")
    print()
    print("  Decision matrix (community-weighted evidence):")
    print(f"    {'weight':>6}  {'stance':<8} {'yr':<5} source")
    for row in d.matrix:
        print(f"    {row.weight:>6.3f}  {row.stance:<8} {row.year:<5} {row.source}")
    print()
    if d.adversary.flags:
        print("  Adversary (fights the easy answer):")
        for f in d.adversary.flags:
            print(f"    [{f.severity.upper():<6}] {f.code}: {f.detail}")
        if d.adversary.strongest_dissent:
            print(f"    strongest dissent -> {d.adversary.strongest_dissent}")
    else:
        print("  Adversary: no flags — consensus survived the challenge.")
    print()


def main() -> None:
    records = load_corpus(CORPUS)
    print(f"Loaded {len(records)} scholarly records (data only; never executed).\n")
    for question, topic in QUESTIONS:
        show(deliberate(question, topic, records, log_path=str(LOG)))
    print(BAR)
    print(f"Full reproducible basis for every decision -> {LOG.name}")


if __name__ == "__main__":
    main()
