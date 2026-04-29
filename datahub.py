"""
Gestion de différentes sources de données (ex : puissance, vitesse, BPM, etc.)
"""
import threading
from dataclasses import dataclass
from collections import deque

@dataclass
class MetricBuffer:
    times: deque
    values: deque

buffers = {
    "hr": MetricBuffer(deque(), deque()),
    "rr": MetricBuffer(deque(), deque()),
    "power": MetricBuffer(deque(), deque()),
    "cadence": MetricBuffer(deque(), deque()),
    "speed": MetricBuffer(deque(), deque())
}

# Global lock
data_lock = threading.Lock()