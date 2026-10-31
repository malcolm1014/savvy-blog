"""
adversary.py — the independent opposition ("fight against it").

Its only job is to attack the comfortable answer: find the strongest dissent,
and raise a flag when the consensus is contested, thin, built on weak sources,
or possibly shifting. It is deliberately separate from the scorers so it is not
the optimist grading its own homework. Any flag it raises pushes the decision
toward human review.
"""

from dataclasses import dataclass, field
from typing import List

from .corpus import Evidence
from .policy import Policy
from .scoring import ScorerResult, base_reflection, _recency_factor, CURRENT_YEAR


@dataclass
class Flag:
    code: str
    severity: str          # "high" | "medium"
    detail: str


@dataclass
class AdversaryReport:
    flags: List[Flag] = field(default_factory=list)
    strongest_dissent: str = ""

    @property
    def high_severity(self) -> bool:
        return any(f.severity == "high" for f in self.flags)


def challenge(records: List[Evidence], ensemble: List[ScorerResult],
              majority_stance: str, policy: Policy) -> AdversaryReport:
    rep = AdversaryReport()

    # Weight everything once with a neutral (citation-leaning) lens for auditing.
    lens = policy.scorers[0]
    weighted = [(e, base_reflection(e, policy, lens)) for e in records]
    total = sum(w for _, w in weighted) or 1e-9

    minority_stances = {"support", "refute", "qualify"} - {majority_stance}
    minority = [(e, w) for e, w in weighted if e.stance in minority_stances]
    minority_share = sum(w for _, w in minority) / total

    # 1) Contested: a meaningful, well-weighted minority exists.
    if minority_share >= policy.contested_minority_share:
        rep.flags.append(Flag(
            "CONTESTED", "high",
            f"Dissenting evidence holds {minority_share:.0%} of weighted support."))
        if minority:
            top = max(minority, key=lambda t: t[1])[0]
            rep.strongest_dissent = f"{top.authors} ({top.year}): {top.finding}"

    # 2) Thin: too few independent groups behind the majority.
    maj_groups = len({e.group for e in records if e.stance == majority_stance})
    if maj_groups < policy.min_independent_groups:
        rep.flags.append(Flag(
            "THIN_EVIDENCE", "high",
            f"Majority rests on {maj_groups} independent group(s); "
            f"need >= {policy.min_independent_groups}."))

    # 3) Low provenance: majority leans on non-peer-reviewed sources.
    maj = [e for e in records if e.stance == majority_stance]
    if maj:
        peer = sum(1 for e in maj if e.provenance == "peer_reviewed")
        if peer / len(maj) < 0.5:
            rep.flags.append(Flag(
                "WEAK_PROVENANCE", "medium",
                "Majority rests mostly on preprints/industry/unknown sources."))

    # 4) Possible shift: the most recent strong work leans against the majority.
    recent = sorted(records, key=lambda e: e.year, reverse=True)[:3]
    recent_against = [e for e in recent
                      if e.stance != majority_stance
                      and _recency_factor(e.year, policy.recency_half_life) > 0.85
                      and e.venue_tier <= 2]
    if len(recent_against) >= 2:
        rep.flags.append(Flag(
            "POSSIBLE_SHIFT", "medium",
            "Two+ recent high-quality sources dissent — consensus may be moving."))

    return rep
