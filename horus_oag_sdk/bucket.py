from __future__ import annotations

from typing import Dict
from dataclasses import dataclass, field


@dataclass
class Bucket:
    buckets: Dict[str, dict] = field(default_factory=dict)

current_bucket = Bucket()

__all__ = ("Bucket",
           "current_bucket")
