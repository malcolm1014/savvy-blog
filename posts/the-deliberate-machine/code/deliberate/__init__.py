"""Deliberate — a consensus decision-matrix engine over scholarly evidence.

Safe-by-construction: corpus is data only (no exec), the core policy is frozen
at deploy, an independent adversary challenges every result, and low-confidence
or contested decisions escalate to a human instead of acting.
"""
from .policy import POLICY, Policy
from .corpus import load_corpus, Evidence, for_topic
from .engine import deliberate, Decision

__all__ = ["POLICY", "Policy", "load_corpus", "Evidence", "for_topic",
           "deliberate", "Decision"]
__version__ = "1.0.0"
