"""
corpus.py — load scholarly records as DATA (never code).

Each record is one claim a source makes about a question, with the provenance
needed to weight it. Loading never evaluates, imports, or executes anything
from the file; corpus content cannot steer the engine except as scored data.
"""

import json
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any

STANCES = {"support", "refute", "qualify"}


@dataclass(frozen=True)
class Evidence:
    id: str
    topic: str                 # which question this bears on
    title: str
    authors: str
    year: int
    venue: str
    venue_tier: int            # 1..3
    citations: int             # illustrative in sample data
    provenance: str            # key into PROVENANCE_TRUST
    group: str                 # research group, for independence accounting
    stance: str                # support | refute | qualify  (re: the question)
    finding: str               # one-line paraphrase of what the source shows

    def validate(self) -> None:
        if self.stance not in STANCES:
            raise ValueError(f"{self.id}: bad stance {self.stance!r}")
        if self.venue_tier not in (1, 2, 3):
            raise ValueError(f"{self.id}: bad venue_tier {self.venue_tier}")


def load_corpus(path: str | Path) -> List[Evidence]:
    """Read a JSON corpus file. Data only: no eval/exec, no network."""
    raw: List[Dict[str, Any]] = json.loads(Path(path).read_text(encoding="utf-8"))
    records: List[Evidence] = []
    for r in raw:
        ev = Evidence(
            id=str(r["id"]),
            topic=str(r["topic"]),
            title=str(r["title"]),
            authors=str(r["authors"]),
            year=int(r["year"]),
            venue=str(r["venue"]),
            venue_tier=int(r["venue_tier"]),
            citations=int(r.get("citations", 0)),
            provenance=str(r.get("provenance", "unknown")),
            group=str(r.get("group", r["id"])),
            stance=str(r["stance"]),
            finding=str(r["finding"]),
        )
        ev.validate()
        records.append(ev)
    return records


def for_topic(records: List[Evidence], topic: str) -> List[Evidence]:
    return [e for e in records if e.topic == topic]
