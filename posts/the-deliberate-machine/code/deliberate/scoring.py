"""
scoring.py — community-reflection weighting and consensus.

"Most accurate data reflected by the community" is made concrete here as a
transparent, auditable weight per source: how it was vetted (provenance),
where it was published (venue tier), how much the field has built on it
(citations), and how current it is (recency) — with independent corroboration
counted across research groups, not double-counted within one.

Each ScorerProfile is one decorrelated 'tree'. We run all of them; agreement
across them is a reliability signal (Section 03 of the brief).
"""

import math
from dataclasses import dataclass
from typing import Dict, List

from .corpus import Evidence
from .policy import Policy, ScorerProfile

CURRENT_YEAR = 2026


def _citation_norm(citations: int) -> float:
    # log-scaled so a 10k-cite paper doesn't dwarf everything; capped at ~1.
    return min(1.0, math.log1p(max(0, citations)) / math.log1p(5000))


def _recency_factor(year: int, half_life: float) -> float:
    age = max(0, CURRENT_YEAR - year)
    return 0.5 + 0.5 * math.exp(-age / half_life)


def base_reflection(ev: Evidence, policy: Policy, scorer: ScorerProfile) -> float:
    """One source's community-reflection weight under one scorer's emphasis."""
    prov = policy.provenance_trust.get(ev.provenance, 0.3)
    venue = policy.venue_tier_weight.get(ev.venue_tier, 0.6)
    cite = _citation_norm(ev.citations)
    rec = _recency_factor(ev.year, policy.recency_half_life)
    signal = (scorer.w_citation * cite
              + scorer.w_venue * venue
              + scorer.w_recency * rec)
    return prov * signal


def _independent_group_weight(items: List[tuple[Evidence, float]], decay: float) -> float:
    """Sum weights with diminishing returns inside a single research group."""
    by_group: Dict[str, List[float]] = {}
    for ev, w in items:
        by_group.setdefault(ev.group, []).append(w)
    total = 0.0
    for weights in by_group.values():
        for rank, w in enumerate(sorted(weights, reverse=True)):
            total += w * (decay ** rank)
    return total


@dataclass
class ScorerResult:
    scorer: str
    support: float
    refute: float
    qualify: float
    net: float            # (support - refute) / total, in [-1, 1]
    verdict: str          # SUPPORTED | REFUTED | CONTESTED
    independent_groups_majority: int


def run_scorer(records: List[Evidence], policy: Policy, scorer: ScorerProfile) -> ScorerResult:
    weighted = [(ev, base_reflection(ev, policy, scorer)) for ev in records]
    sup = [(e, w) for e, w in weighted if e.stance == "support"]
    ref = [(e, w) for e, w in weighted if e.stance == "refute"]
    qual = [(e, w) for e, w in weighted if e.stance == "qualify"]

    s = _independent_group_weight(sup, policy.within_group_decay)
    r = _independent_group_weight(ref, policy.within_group_decay)
    q = _independent_group_weight(qual, policy.within_group_decay)
    total = s + r + q or 1e-9
    net = (s - r) / total

    if net >= 0.34:
        verdict = "SUPPORTED"
        groups = len({e.group for e, _ in sup})
    elif net <= -0.34:
        verdict = "REFUTED"
        groups = len({e.group for e, _ in ref})
    else:
        verdict = "CONTESTED"
        groups = len({e.group for e, _ in (sup if s >= r else ref)})

    return ScorerResult(scorer.name, s, r, q, net, verdict, groups)


def run_ensemble(records: List[Evidence], policy: Policy) -> List[ScorerResult]:
    """All decorrelated scorers (the polymorphic trees)."""
    return [run_scorer(records, policy, sc) for sc in policy.scorers]
