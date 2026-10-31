"""
policy.py — the inherited core ("genetic memory").

These weights and thresholds are the frozen, reviewed decision policy the
engine is born with. In the architecture this file is the part that is
trained/tuned in a sealed environment and then promoted deliberately as a new
version. In production it does NOT change itself from live corpus input —
retraining produces a new POLICY_VERSION, reviewed before deployment.

Nothing here executes corpus content. The corpus is data, never code.
"""

from dataclasses import dataclass, field
from typing import Dict, List

POLICY_VERSION = "1.0.0-frozen"

# --- how much a source's "community reflection" counts ---------------------
# Trust by how the work was vetted. Low-provenance sources are down-weighted,
# not silently trusted — this is the corpus trust-gate in miniature.
PROVENANCE_TRUST: Dict[str, float] = {
    "peer_reviewed": 1.00,
    "preprint": 0.75,
    "industry_report": 0.70,
    "unknown": 0.30,
}

# Venue tier multiplier (1 = flagship/top, 3 = minor). Transparent, auditable.
VENUE_TIER_WEIGHT: Dict[int, float] = {1: 1.00, 2: 0.80, 3: 0.60}

# Recency: knowledge compounds, so decay is gentle, not harsh.
RECENCY_HALF_LIFE_YEARS = 6.0

# Diminishing returns *within* one research group, so five papers from the
# same lab count as (nearly) one independent voice, not five.
WITHIN_GROUP_DECAY = 0.55


@dataclass(frozen=True)
class ScorerProfile:
    """One 'polymorphic tree': a scorer that emphasizes a different signal.
    Running several decorrelated scorers and checking whether they agree is
    the ensemble/uncertainty mechanism — disagreement is a reliability flag."""
    name: str
    w_citation: float
    w_venue: float
    w_recency: float


# Three decorrelated scorers. Each reaches its verdict a different way, so when
# all three agree the consensus is robust; when they split, that split is
# itself a measured signal that the evidence is shaky.
SCORERS: List[ScorerProfile] = [
    ScorerProfile("citation-weighted", w_citation=0.60, w_venue=0.25, w_recency=0.15),
    ScorerProfile("recency-weighted",  w_citation=0.20, w_venue=0.25, w_recency=0.55),
    ScorerProfile("venue-weighted",    w_citation=0.25, w_venue=0.55, w_recency=0.20),
]

# --- thresholds that govern autonomy ---------------------------------------
# These four together are the single real dial of the system: how strong the
# opposition must be before a comfortable answer is allowed through.
CONFIDENCE_AUTONOMOUS = 0.70     # below this -> escalate to a human
CONTESTED_MINORITY_SHARE = 0.25  # dissent this large -> flag contested
MIN_INDEPENDENT_GROUPS = 2       # fewer independent voices -> flag thin
ENSEMBLE_AGREEMENT_MIN = 0.67    # scorers must mostly agree, else flag split


@dataclass(frozen=True)
class Policy:
    version: str = POLICY_VERSION
    provenance_trust: Dict[str, float] = field(default_factory=lambda: dict(PROVENANCE_TRUST))
    venue_tier_weight: Dict[int, float] = field(default_factory=lambda: dict(VENUE_TIER_WEIGHT))
    recency_half_life: float = RECENCY_HALF_LIFE_YEARS
    within_group_decay: float = WITHIN_GROUP_DECAY
    scorers: List[ScorerProfile] = field(default_factory=lambda: list(SCORERS))
    confidence_autonomous: float = CONFIDENCE_AUTONOMOUS
    contested_minority_share: float = CONTESTED_MINORITY_SHARE
    min_independent_groups: int = MIN_INDEPENDENT_GROUPS
    ensemble_agreement_min: float = ENSEMBLE_AGREEMENT_MIN


POLICY = Policy()
