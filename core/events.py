from dataclasses import dataclass

@dataclass
class MetricEvent:
    t: float
    metric: str
    value: float
    source: str