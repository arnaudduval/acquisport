from dataclasses import dataclass
from typing import Optional


@dataclass
class SampleEvent:
    t: float | None = None
    hr: Optional[float] = None
    power: Optional[float] = None
    cadence: Optional[float] = None
    speed: Optional[float] = None
    source: str = "unknown"