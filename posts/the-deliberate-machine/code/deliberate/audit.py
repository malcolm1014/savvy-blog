"""
audit.py — the trail that makes a decision reproducible.

Every decision writes its full basis to an append-only JSONL log: the policy
version it ran under, the matrix, the ensemble, the adversary flags, and the
final routing. This is the auditability pillar — nothing about the verdict is
hidden inside an opaque pass.
"""

import json
from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _plain(obj: Any) -> Any:
    if is_dataclass(obj) and not isinstance(obj, type):
        return {k: _plain(v) for k, v in asdict(obj).items()}
    if isinstance(obj, dict):
        return {k: _plain(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_plain(v) for v in obj]
    return obj


def record(decision: Any, log_path: str | Path = "audit_log.jsonl") -> None:
    entry = {
        "logged_at": datetime.now(timezone.utc).isoformat(),
        "decision": _plain(decision),
    }
    with Path(log_path).open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
