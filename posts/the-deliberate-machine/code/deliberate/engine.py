"""
engine.py — orchestrates one deliberation.

Flow for a question:
  1. select relevant scholarly evidence (data only),
  2. run the decorrelated scorers (the polymorphic trees),
  3. build an auditable decision matrix weighted by community reflection,
  4. let the independent adversary attack the result,
  5. route: AUTONOMOUS if strong and unchallenged, else REVIEW_REQUIRED.

It never acts on the world and never auto-deploys. It emits a verdict, a
confidence, the full basis, and — when the evidence is thin or contested —
an explicit hand-off to a human. That is the earned, bounded autonomy the
whole architecture was built around.
"""

from collections import Counter
from dataclasses import dataclass, field
from typing import List

from .corpus import Evidence, for_topic
from .policy import POLICY, Policy
from .scoring import ScorerResult, run_ensemble, base_reflection
from .adversary import AdversaryReport, challenge
from . import audit


@dataclass
class MatrixRow:
    source: str
    year: int
    stance: str
    weight: float
    provenance: str
    finding: str


@dataclass
class Decision:
    policy_version: str
    question: str
    verdict: str                      # SUPPORTED | REFUTED | CONTESTED | NO_EVIDENCE
    confidence: float                 # 0..1
    routing: str                      # AUTONOMOUS | REVIEW_REQUIRED
    ensemble_agreement: float
    ensemble: List[ScorerResult]
    matrix: List[MatrixRow]
    adversary: AdversaryReport
    reason: str = ""
    notes: List[str] = field(default_factory=list)


def _confidence(net_abs: float, agreement: float, adversary: AdversaryReport,
                policy: Policy) -> float:
    c = net_abs                                 # strength of the consensus
    c *= 0.55 + 0.45 * agreement                # scorers must agree
    for f in adversary.flags:                   # opposition erodes trust
        c -= 0.25 if f.severity == "high" else 0.10
    return max(0.0, min(1.0, c))


def deliberate(question: str, topic: str, records: List[Evidence],
               policy: Policy = POLICY, log_path: str | None = "audit_log.jsonl") -> Decision:
    relevant = for_topic(records, topic)

    if not relevant:
        dec = Decision(policy.version, question, "NO_EVIDENCE", 0.0,
                       "REVIEW_REQUIRED", 0.0, [], [],
                       AdversaryReport(), reason="No scholarly evidence on file for this topic.")
        if log_path:
            audit.record(dec, log_path)
        return dec

    ensemble = run_ensemble(relevant, policy)
    verdicts = Counter(r.verdict for r in ensemble)
    top_verdict, top_count = verdicts.most_common(1)[0]
    agreement = top_count / len(ensemble)

    majority_stance = {"SUPPORTED": "support", "REFUTED": "refute"}.get(top_verdict, "support")
    net_abs = sum(abs(r.net) for r in ensemble) / len(ensemble)

    adversary = challenge(relevant, ensemble, majority_stance, policy)

    lens = policy.scorers[0]
    matrix = sorted(
        (MatrixRow(f"{e.authors} — {e.title[:48]}", e.year, e.stance,
                   round(base_reflection(e, policy, lens), 3), e.provenance, e.finding)
         for e in relevant),
        key=lambda row: row.weight, reverse=True)

    confidence = _confidence(net_abs, agreement, adversary, policy)

    notes: List[str] = []
    route = "AUTONOMOUS"
    reasons = []
    if top_verdict == "CONTESTED":
        route = "REVIEW_REQUIRED"
        reasons.append("evidence is genuinely contested in the literature")
    elif agreement < policy.ensemble_agreement_min:
        route = "REVIEW_REQUIRED"
        reasons.append(f"decorrelated scorers disagree (agreement {agreement:.0%})")
    if adversary.high_severity:
        route = "REVIEW_REQUIRED"
        reasons.append("adversary raised a high-severity flag")
    if confidence < policy.confidence_autonomous:
        route = "REVIEW_REQUIRED"
        reasons.append(f"confidence {confidence:.2f} below {policy.confidence_autonomous:.2f}")

    if route == "AUTONOMOUS":
        notes.append("Handled autonomously: strong, corroborated, unchallenged.")
    else:
        notes.append("Escalated to a human — see reason and adversary flags.")

    dec = Decision(
        policy_version=policy.version, question=question,
        verdict=top_verdict, confidence=round(confidence, 3), routing=route,
        ensemble_agreement=round(agreement, 3), ensemble=ensemble, matrix=matrix,
        adversary=adversary, reason="; ".join(reasons) or "clear consensus", notes=notes)

    if log_path:
        audit.record(dec, log_path)
    return dec
